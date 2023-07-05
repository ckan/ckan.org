from django.conf import settings
from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail import blocks

from wagtailmetadata.models import MetadataPageMixin
from wagtailcodeblock.blocks import CodeBlock


COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('search_description'),
    FieldPanel('keywords'),
    FieldPanel('search_image'),
)


class FaqPage(MetadataPageMixin, Page):
    """Frequently Asked Questions Base Page"""
    parent_page_types = ['home.HomePage']
    subpage_types = ['faq.FaqCategoryPage', 'faq.FaqQuestionPage']
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
    ]

    class Meta:
        verbose_name = 'FAQ page'
        verbose_name_plural = 'FAQ pages'

    def get_context(self,request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['categories'] = FaqCategoryPage.objects.all()
        context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class FaqCategoryPage(MetadataPageMixin, Page):
    """FAQ Category Model"""
    parent_page_types = ['faq.FaqPage']
    subpage_types = []

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text='Name of questions groupping.',
    )
    description = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        help_text='Short description of a category.',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text="Image for displaying near category name on the main FAQ page.",
        on_delete=models.SET_NULL,
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
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('image'),
    ]

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_context(self,request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['questions'] = FaqQuestionPage.objects.all().filter(category=self.id)
        context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class FaqQuestionPage(MetadataPageMixin, Page):
    """FAQ Question with Answer Model"""
    parent_page_types = ['faq.FaqPage']
    subpage_types = []

    category = models.ForeignKey(
        FaqCategoryPage, 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='faq_category'
    )
    question = models.CharField(
        max_length=512,
        unique=True
    )
    answer = StreamField([
            ('paragraph', blocks.RichTextBlock(
                features=[
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'bold', 'italic', 'ol', 'ul', 'hr', 'image', 'embed',
                    'link', 'document-link', 'code',
                    'superscript', 'subscript', 'strikethrough','blockquote',
                ])),
            ('code', CodeBlock(label='Code')),
        ],
        null=True,
        blank=True
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
        FieldPanel('category'),
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    def get_context(self,request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
        return context