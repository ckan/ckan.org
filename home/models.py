from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from modelcluster.fields import ParentalKey

from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtailmetadata.models import MetadataPageMixin
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel
)

from streams.models import GitCardBlock
from ckan_pages.models import CkanForPage

import posthog


COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('search_description'),
    FieldPanel('keywords'),
    FieldPanel('search_image'),
)


class CkanForHomeOrderable(Orderable):

    page = ParentalKey('home.HomePage', related_name='ckan_for_cards')
    ckan_for_card = models.ForeignKey(
        'streams.CkanForCard',
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel('ckan_for_card'),
    ]


class PoweredCardHomeOrderable(Orderable):

    page = ParentalKey('home.HomePage', related_name='powered_cards')
    powered_card = models.ForeignKey(
        'streams.PoweredCard',
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel('powered_card'),
    ]


class PoweringImages(Orderable):

    page = ParentalKey('home.HomePage', related_name='powering_images')
    powering_image = models.ForeignKey(
        'streams.PoweringImage',
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel('powering_image'),
    ]


class HomePage(MetadataPageMixin, Page):

    parent_page_types = ['wagtailcore.Page']
    subpage_types = [
        'contact.ContactPage',
        'ckan_pages.FeaturesPage',
        'ckan_pages.ShowcasePage',
        'ckan_pages.CommunityPage',
        'ckan_pages.CommercialPage',
        'ckan_pages.CkanForPage',
        'blog.BlogListingPage',
        'events.EventListingPage',
        'faq.FaqPage',
    ]
    max_count = 1

    favicon = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='Favicon (16x16) for the site',
        on_delete=models.SET_NULL,
    )

    home_page_subtitle = models.CharField(
        max_length=512,
        blank=True,
        null=False,
        help_text='Subtitle text under the header',
    )

    keywords = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )

    ckan_git = StreamField(
        blocks.StreamBlock([
            ('cards', GitCardBlock())
        ], max_num=1, min_num=1),
        blank=False,
        null=True,
        help_text='CKAN Git section',
        use_json_field=True
    )

    home_page_subtitle_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='The image that goes under the home page subtitle',
        on_delete=models.SET_NULL,
    )

    promote_panels = [
            MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
        ]

    content_panels = Page.content_panels + [
        FieldPanel('favicon'),
        FieldPanel('home_page_subtitle'),
        FieldPanel('ckan_git'),
        MultiFieldPanel(
            [
                InlinePanel('powering_images', label="Powering open data item", min_num=1),
            ],
            heading='Powering open data Images',
        ),
        MultiFieldPanel(
            [
                InlinePanel('ckan_for_cards', label="Card", min_num=2, max_num=2),
            ],
            heading='CKAN for ... Cards',
        ),
        MultiFieldPanel(
            [
                InlinePanel('powered_cards', label="Card", min_num=2, max_num=12),
            ],
            heading='Powered by CKAN Cards',
        ),
    ]

    def get_context(self,request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        ckan_for_government = CkanForPage.objects.live(
            ).public().filter(page_for='government')
        context['ckan_for_government_page'] = ckan_for_government[0] if ckan_for_government else None
        ckan_for_enterprise = CkanForPage.objects.live(
            ).public().filter(page_for='enterprise')
        context['ckan_for_enterprise_page'] = ckan_for_enterprise[0] if ckan_for_enterprise else None
        showcase = Page.objects.live(
            ).public().filter(title='Showcase')
        context['showcase_page'] = showcase[0] if showcase else None
        community = Page.objects.live(
            ).public().filter(title='Community')
        context['community_page'] = community[0] if community else None
        context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY

        posthog.capture('test-id', 'test-event')

        return context

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Blog Post Creators')
        instance.groups.add(group)

@register_setting
class ReCaptchaSettings(BaseSiteSetting):
    public_key = models.CharField(
        max_length=255,
        help_text="ReCaptcha public key",
        blank=True,
    )

    class Meta:
        verbose_name = 'ReCaptcha settings'
        verbose_name_plural = "ReCaptcha settings"

    panels = [
        FieldPanel('public_key'),
    ]


@register_setting
class PostHogSettings(BaseSiteSetting):
    api_key = models.CharField(
        max_length=255,
        help_text="PostHog API key",
        blank=True,
    )
    host = models.CharField(
        max_length=255,
        help_text="PostHog host address",
        blank=True,
    )

    class Meta:
        verbose_name = 'PostHog settings'
        verbose_name_plural = "PostHog settings"

    panels = [
        FieldPanel('api_key'),
        FieldPanel('host'),
    ]
