from django import forms
from django.conf import settings
from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable

from modelcluster.fields import ParentalKey
from wagtailmetadata.models import MetadataPageMixin

from blog.models import BlogPostPage


COMMON_PANELS = (
    FieldPanel("slug"),
    FieldPanel("seo_title"),
    FieldPanel("search_description"),
    FieldPanel("keywords"),
    FieldPanel("search_image"),
)


class GeneralFeatures(Orderable):

    page = ParentalKey("ckan_pages.FeaturesPage", related_name="general_features")
    feature = models.ForeignKey(
        "streams.GeneralFeature",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("feature"),
    ]


class Features(Orderable):

    page = ParentalKey("ckan_pages.FeaturesPage", related_name="features")
    feature = models.ForeignKey(
        "streams.Feature",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("feature"),
    ]


class Extensions(Orderable):

    page = ParentalKey("ckan_pages.FeaturesPage", related_name="extensions")
    extension = models.ForeignKey(
        "streams.Extension",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("extension"),
    ]


class CkanForFeatures(Orderable):

    page = ParentalKey("ckan_pages.FeaturesPage", related_name="ckan_for_cards")
    ckan_for_card = models.ForeignKey(
        "streams.CkanForCard",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("ckan_for_card"),
    ]


class FeaturesPage(MetadataPageMixin, Page):

    parent_page_types = ["home.HomePage"]
    subpage_types = ["ckan_pages.FeatureDetailPage"]
    max_count = 1

    page_subtitle = models.CharField(
        max_length=512,
        blank=True,
        null=False,
        help_text="Subtitle text",
    )

    keywords = models.CharField(max_length=512, blank=True, null=True)

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("page_subtitle"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "general_features", label="General Feature", min_num=2, max_num=4
                ),
            ],
            heading="General Features",
        ),
        MultiFieldPanel(
            [
                InlinePanel("features", label="Feature", min_num=2, max_num=12),
            ],
            heading="Features",
        ),
        MultiFieldPanel(
            [
                InlinePanel("extensions", label="Extension", min_num=3),
            ],
            heading="Extension",
        ),
        MultiFieldPanel(
            [
                InlinePanel("ckan_for_cards", label="Card", min_num=2, max_num=2),
            ],
            heading="CKAN for ... Cards",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class ShowCaseSection1(Orderable):

    page = ParentalKey("ckan_pages.ShowcasePage", related_name="showcase_section_1")
    showcase = models.ForeignKey(
        "streams.PoweredCard",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("showcase"),
    ]


class ShowCaseSection2(Orderable):

    page = ParentalKey("ckan_pages.ShowcasePage", related_name="showcase_section_2")
    showcase = models.ForeignKey(
        "streams.PoweredCard",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("showcase"),
    ]


class ShowCaseSection3(Orderable):

    page = ParentalKey("ckan_pages.ShowcasePage", related_name="showcase_section_3")
    showcase = models.ForeignKey(
        "streams.PoweredCard",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("showcase"),
    ]


class FeedbackSection1(Orderable):

    page = ParentalKey("ckan_pages.ShowcasePage", related_name="feedback_section_1")
    feedback = models.ForeignKey(
        "streams.Feedback",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("feedback"),
    ]


class FeedbackSection2(Orderable):

    page = ParentalKey("ckan_pages.ShowcasePage", related_name="feedback_section_2")
    feedback = models.ForeignKey(
        "streams.Feedback",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("feedback"),
    ]


class ShowcasePage(MetadataPageMixin, Page):

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    page_subtitle = models.CharField(
        max_length=512,
        blank=True,
        null=False,
        help_text="Subtitle text",
    )

    keywords = models.CharField(max_length=512, blank=True, null=True)

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("page_subtitle"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "showcase_section_1", label="Showcase", min_num=2, max_num=10
                ),
            ],
            heading="Showcase section 1",
        ),
        MultiFieldPanel(
            [
                InlinePanel("feedback_section_1", label="Feedback", min_num=1),
            ],
            heading="Feedback section 1",
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "showcase_section_2", label="Showcase", min_num=2, max_num=10
                ),
            ],
            heading="Showcase section 2",
        ),
        MultiFieldPanel(
            [
                InlinePanel("feedback_section_2", label="Feedback", min_num=1),
            ],
            heading="Feedback section 2",
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "showcase_section_3", label="Showcase", min_num=2, max_num=10
                ),
            ],
            heading="Showcase section 3",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class SoftwareEngineers(Orderable):

    page = ParentalKey("ckan_pages.CommunityPage", related_name="developers")
    developer = models.ForeignKey(
        "streams.SoftwareEngineer",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("developer"),
    ]


class Stewards(Orderable):

    page = ParentalKey("ckan_pages.CommunityPage", related_name="stewards")
    steward = models.ForeignKey(
        "streams.Steward",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("steward"),
    ]


class WorkingGroups(Orderable):

    page = ParentalKey("ckan_pages.CommunityPage", related_name="working_groups")
    working_group = models.ForeignKey(
        "streams.WorkingGroup",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("working_group"),
    ]


class CommunityPage(MetadataPageMixin, Page):

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    contributors_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        related_name="+",
        help_text="Contributors' photos",
        on_delete=models.SET_NULL,
    )

    subtitle = models.CharField(
        max_length=512,
        blank=True,
        null=False,
        help_text="Subtitle text under the header",
    )

    tech_team_title = models.CharField(
        max_length=256,
        blank=True,
        null=False,
        help_text="The Tech Team block title",
    )

    tech_team_subtitle = models.TextField(
        max_length=1024,
        blank=True,
        null=False,
        help_text="The Tech Team block subtitle",
    )

    stewards_title = models.CharField(
        max_length=256,
        blank=True,
        null=False,
        help_text="The CKAN Stewards block title",
    )

    stewards_subtitle = models.TextField(
        max_length=1024,
        blank=True,
        null=False,
        help_text="The CKAN Stewards block subtitle",
    )

    open_knowledge_foundation_title = models.CharField(
        max_length=256,
        blank=True,
        null=False,
        help_text="Open Knowledge Foundation block title",
    )

    open_knowledge_foundation_subtitle = models.TextField(
        max_length=1024,
        blank=True,
        null=False,
        help_text="Open Knowledge Foundation block subtitle",
    )

    open_knowledge_foundation_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        related_name="+",
        help_text="Open Knowledge Foundation block image",
        on_delete=models.SET_NULL,
    )

    working_groups_title = models.CharField(
        max_length=256,
        blank=True,
        null=False,
        help_text="Working groups block title",
    )

    working_groups_subtitle = models.TextField(
        max_length=1024,
        blank=True,
        null=False,
        help_text="Working groups block subtitle",
    )

    keywords = models.CharField(max_length=512, blank=True, null=True)

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("contributors_image"),
        FieldPanel("subtitle"),
        MultiFieldPanel(
            [
                FieldPanel("tech_team_title"),
                FieldPanel("tech_team_subtitle"),
            ],
            heading="The Tech team section heading",
        ),
        MultiFieldPanel(
            [
                InlinePanel("developers", label="Developers", min_num=3),
            ],
            heading="Software Engineers",
        ),
        MultiFieldPanel(
            [
                FieldPanel("stewards_title"),
                FieldPanel("stewards_subtitle"),
            ],
            heading="The CKAN Stewards section heading",
        ),
        MultiFieldPanel(
            [
                InlinePanel("stewards", label="Steward", min_num=1),
            ],
            heading="Stewards",
        ),
        MultiFieldPanel(
            [
                FieldPanel("open_knowledge_foundation_title"),
                FieldPanel("open_knowledge_foundation_subtitle"),
                FieldPanel("open_knowledge_foundation_image"),
            ],
            heading="Open Knowledge Foundation section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("working_groups_title"),
                FieldPanel("working_groups_subtitle"),
            ],
            heading="Working groups section",
        ),
        MultiFieldPanel(
            [
                InlinePanel("working_groups", label="Working Group", min_num=1),
            ],
            heading="Working Groups",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class CommercialSupportItem(Orderable):

    page = ParentalKey("ckan_pages.CommercialPage", related_name="commercial")
    commercial = models.ForeignKey(
        "streams.Commercial",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("commercial"),
    ]


class CommercialPage(MetadataPageMixin, Page):

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    subtitle = models.CharField(
        max_length=512,
        blank=True,
        null=False,
        help_text="Subtitle text under the header",
    )

    keywords = models.CharField(max_length=512, blank=True, null=True)

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        MultiFieldPanel(
            [
                InlinePanel("commercial", label="Commercial", min_num=1),
            ],
            heading="Commercial",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)


class PweredItems(Orderable):

    page = ParentalKey("ckan_pages.CkanForPage", related_name="powered_items")
    powered_item = models.ForeignKey(
        "streams.PoweredCard",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("powered_item"),
    ]


class FeedbackItems(Orderable):

    page = ParentalKey("ckan_pages.CkanForPage", related_name="feedback_items")
    feedback_item = models.ForeignKey(
        "streams.Feedback",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("feedback_item"),
    ]


class WorkingGroupItems(Orderable):

    page = ParentalKey("ckan_pages.CkanForPage", related_name="group_items")
    group_item = models.ForeignKey(
        "streams.WorkingGroup",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("group_item"),
    ]


class CkanForPage(MetadataPageMixin, Page):

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 2

    page_for = models.CharField(
        max_length=512,
        help_text="CKAN for: government / enterprise",
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        related_name="+",
        help_text="Main image",
        on_delete=models.SET_NULL,
    )

    page_title = models.CharField(
        max_length=512,
        default="Page title",
        help_text="Page title",
    )

    subtitle = models.CharField(
        max_length=512,
        blank=True,
        null=False,
        help_text="Subtitle text under the header",
    )

    upper_text = models.TextField(
        max_length=2056, blank=True, null=False, help_text="Upper text block"
    )

    keywords = models.CharField(max_length=512, blank=True, null=True)

    bottom_text = StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(
                    features=[
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "h5",
                        "h6",
                        "bold",
                        "italic",
                        "link",
                        "ol",
                        "ul",
                        "hr",
                    ]
                ),
            ),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("page_for"),
        FieldPanel("image"),
        FieldPanel("page_title"),
        FieldPanel("subtitle"),
        FieldPanel("upper_text"),
        MultiFieldPanel(
            [
                InlinePanel("powered_items", label="Powered by CKAN items", min_num=2),
            ],
            heading="Powered by CKAN",
        ),
        MultiFieldPanel(
            [
                InlinePanel("feedback_items", label="Feedback", min_num=1),
            ],
            heading="Feedbacks",
        ),
        MultiFieldPanel(
            [
                InlinePanel("group_items", label="Working Group", min_num=1, max_num=1),
            ],
            heading="Working Group",
        ),
        FieldPanel("bottom_text"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blog_posts"] = (
            BlogPostPage.objects.filter(tags__name__in=[self.page_for.capitalize()])
            .live()
            .public()
            .order_by("-created")[:2]
        )
        flt = "government" if self.page_for == "enterprise" else "enterprise"
        bottom_block_page = CkanForPage.objects.live().public().filter(page_for=flt)
        context["bottom_block_page"] = (
            bottom_block_page[0] if bottom_block_page else None
        )
        community = Page.objects.live().public().filter(title="Community")
        context["community_page"] = community[0] if community else None
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class FeatureDetailPage(MetadataPageMixin, Page):

    parent_page_types = ["ckan_pages.FeaturesPage"]
    subpage_types = []

    subtitle = models.CharField(
        max_length=512,
        blank=True,
        null=False,
        help_text="Subtitle text under the header",
    )
    keywords = models.CharField(max_length=512, blank=True, null=True)
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context
