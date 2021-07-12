from datetime import datetime, timezone
from django.utils.timezone import now

from django import forms
from django.db import models
from django.core.validators import MinValueValidator
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator
)

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtailmetadata.models import MetadataPageMixin

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import TaggedItemBase

from .blocks import ImageWithCaption

import events


COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('search_description'),
    FieldPanel('keywords'),
    ImageChooserPanel('search_image'),
)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPostPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class BlogListingPage(MetadataPageMixin, Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPostPage']
    max_count = 1

    page_subtitle = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text='Page subtitle. Goes under the header.',

    )
    page_caption = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        help_text='Page caption. Goes under the page subtitle.',
    )
    posts_per_page = models.PositiveIntegerField(
        default = 1,
        validators=[MinValueValidator(1)]
    )
    keywords = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )

    promote_panels = [
            MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
        ]
    
    content_panels = Page.content_panels + [
        FieldPanel('page_subtitle'),
        FieldPanel('page_caption'),
        FieldPanel('posts_per_page'),
    ]

    def get_context(self,request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogPostPage.objects.live().public().order_by('-created')
        featured_posts = BlogPostPage.objects.live().public(
            ).filter(featured=True).order_by('-created')
        featured_post = featured_posts[0] if featured_posts else all_posts[0]
        context['featured_post'] = featured_post
        all_posts = all_posts.exclude(id__in=[featured_post.id,])
        paginator = Paginator(all_posts, self.posts_per_page)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        return context


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(
            choices=self.field.widget.choices
        )

class BlogPostPage(MetadataPageMixin, Page):

    parent_page_types = ['blog.BlogListingPage']
    subpage_types = []

    main_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text="Image",
        on_delete=models.SET_NULL,
    )
    author = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        blank=True,
        default=now,
    )
    post_title = models.CharField(
        max_length=512,
        null=True,
        blank=True
    )
    featured = models.BooleanField(
        null=True,
        default=False
    )
    imported = models.BooleanField(
        null=True,
        default=False
    )
    post_subtitle = models.CharField(
        max_length=512,
        null=True,
        blank=True,
    )
    keywords = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )    
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True
    )
    body = StreamField([
        ('html', blocks.RawHTMLBlock()),
        ('paragraph', blocks.RichTextBlock(
            features=[
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'bold', 'italic', 'link', 'ol', 'ul', 'hr'
            ])),
        ('post_image', ImageWithCaption()),
    ],
    null=True,
    blank=True
    )

    promote_panels = [
            MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
        ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('main_image'),
        FieldPanel('post_title'),
        FieldPanel('featured', widget=forms.CheckboxInput),
        FieldPanel('post_subtitle'),
        FieldPanel('tags'),
        StreamFieldPanel('body'),
    ]

    def get_context(self,request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['last_posts'] = BlogPostPage.objects.live().public(
            ).exclude(id__in=[self.id,]).order_by('-created')[:2]
        return context

