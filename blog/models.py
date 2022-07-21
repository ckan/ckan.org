from datetime import datetime, timezone
from django.utils.timezone import now
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django import forms
from django.db import models
from django.core.validators import MinValueValidator, ValidationError
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator
)

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtailmetadata.models import MetadataPageMixin
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.snippets.models import register_snippet

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


# DEPRECATED
def check_username_exists(value):
    if not value:
        raise ValidationError("Author field cannot be empty")
    author = User.objects.filter(username=value).first()
    if not author:
        raise ValidationError("There is not such User with this username.")


class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(
        max_length=500, 
        blank=True
    )
    company = models.CharField(
        max_length=100, 
        blank=True
    )
    location = models.CharField(
        max_length=30, 
        blank=True
    )
    site = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )
    linkedin = models.CharField(
        null=True,
        blank=True,        
        max_length=512,
    )
    github = models.CharField(
        null=True,
        blank=True,        
        max_length=512,
    )
       
    def __str__(self):
        return self.user.username
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('user'),
                FieldPanel('bio'),
                FieldPanel('company'),
                FieldPanel('location'),
                FieldPanel('site'),
                FieldPanel('linkedin'),
                FieldPanel('github'),
            ],
            heading = "User profile"
        )
    ]
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class PostCategoryPage(models.Model):

    category_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text="Image",
        on_delete=models.SET_NULL,
    )
    category_title = models.CharField(
        max_length=512,
        null=True,
        blank=True
    )
    description = StreamField([
        ('paragraph', blocks.RichTextBlock(
            features=[
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'bold', 'italic', 'link', 'ol', 'ul', 'hr'
            ])),
        ],
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.category_title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('category_title'),
                ImageChooserPanel('category_image'),
                StreamFieldPanel('description')
            ]
        )
    ]
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


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
        context['categories'] = PostCategoryPage.objects.all().order_by('-category_title')
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
        help_text='If value is empty, it will be filled by the current User.'
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
    category = models.ForeignKey(
        PostCategoryPage, 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='post_category'
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
        FieldPanel('category'),
        FieldPanel('post_title'),
        FieldPanel('featured', widget=forms.CheckboxInput),
        FieldPanel('post_subtitle'),
        FieldPanel('tags'),
        StreamFieldPanel('body'),
        FieldPanel('author')
    ]

    def get_context(self,request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['last_posts'] = BlogPostPage.objects.live().public(
            ).exclude(id__in=[self.id,]).order_by('-created')[:2]
        author = context.get('page').author
        if author:
            author_user = User.objects.filter(username=author).first()
            if author_user:
                context['blog_author'] = author_user
        return context
