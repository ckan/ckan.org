from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.fields import StreamField
from wagtail.models import Page

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class StoriesPage(Page):
    parent_page_types = ["home.HomePage"]
    template = "stories/stories.html"
    max_count = 1  # Only one stories page
    
    stories_order_by = models.CharField(
        max_length=64,
        default="-created",
        help_text=_("Default ordering for story items (stories_order_by)")
    )

    google_docs_template = models.URLField(
        max_length=512,
        null=True,
        blank=True,
        help_text=_("Google Docs template URL for story submissions (google_docs_template)")
    )

    content_panels = Page.content_panels + [
        FieldPanel("stories_order_by"),
        FieldPanel("google_docs_template"),
    ]

    class Meta: # type: ignore
        verbose_name = _("Stories Page")
        verbose_name_plural = _("Stories Pages")

    @staticmethod
    def _stream_to_repeated_fields(stream_value):
        if not stream_value:
            return []
        out = []
        for block in stream_value:
            if block.block_type == "repeated_fields":
                out.append({
                    "label": block.value.get("label"),
                    "val": block.value.get("value"),
                })
        return out

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Get google docs template URL from settings
        context["google_docs_template"] = self.google_docs_template
        # Fetch all story items
        stories_qs = StoryItem.objects.all().order_by(self.stories_order_by) # type: ignore
        stories = []
        for story in stories_qs:
            stories.append({
                "id": story.id, # type: ignore
                "org": story.org,
                "region": story.region,
                "title": story.title,
                "challenge": story.challenge,
                "tags": list(story.tags.names()) if story.tags else [],
                "color": story.color,
                "emoji": story.emoji,
                "meta": self._stream_to_repeated_fields(story.meta),
                "impact": self._stream_to_repeated_fields(story.impact),
                "who": story.who,
                "how": story.how,
                "outcome": story.outcome,
                "quote": story.quote,
                "quoteAuthor": story.quote_author,
                "portal": story.portal,
            })
        context["stories"] = stories
        # Add reCAPTCHA site key to context
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context


class StoryItemTag(TaggedItemBase):
    content_object = ParentalKey(
        "StoryItem",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class RepeatedFieldsBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=False)
    value = blocks.CharBlock(required=False)

    class Meta: # type: ignore
        icon = "list-ul"
        label = _("Repeated Fields")


class StoryItem(ClusterableModel):
    """Model representing an individual story item, which can be displayed on the StoriesPage.
    """
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Title of the story (title)")
    )
    org = models.CharField(
        verbose_name=_("Organization"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Organization or entity featured in the story (org)")
    )
    region = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text=_("Region or continent (region)")
    )
    challenge = models.TextField(
        null=True,
        blank=True,
        help_text=_("The challenge or problem addressed (challenge)")
    )
    tags = ClusterTaggableManager(
        through=StoryItemTag,
        blank=True,
        help_text=_("The story item this tag is associated with, e.g. gov, ngo, research, civic, health (content_object)")
    )
    color = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text=_("Card color in HEX format (color)")
    )
    emoji = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text=_("Emoji character(s), e.g. 🇬🇧 or 🌐 (emoji)")
    )
    meta = StreamField(
        [
            ("repeated_fields", RepeatedFieldsBlock()),
        ],
        null=True,
        blank=True,
        help_text=_("Additional metadata (meta)")
    )
    impact = StreamField(
        [
            ("repeated_fields", RepeatedFieldsBlock()),
        ],
        null=True,
        blank=True,
        help_text=_("Impact details (impact)")
    )
    who = models.TextField(
        null=True,
        blank=True,
        help_text=_("Who they are (who)")
    )
    how = models.TextField(
        null=True,
        blank=True,
        help_text=_("How CKAN solved it (how)")
    )
    outcome = models.TextField(
        null=True,
        blank=True,
        help_text=_("Impact & outcomes (outcome)")
    )
    quote = models.TextField(
        null=True,
        blank=True,
        help_text=_("Quote (quote)")
    )
    quote_author = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Quote author (quoteAuthor)")
    )
    portal = models.URLField(
        max_length=512,
        null=True,
        blank=True,
        help_text=_("Portal URL (portal)")
    )
    # Optionally, keep legacy fields for compatibility
    created = models.DateTimeField(
        blank=True,
        default=now,
        help_text=_("Date created")
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("org"),
        FieldPanel("region"),
        FieldPanel("challenge"),
        FieldPanel("tags"),
        FieldPanel("color"),
        FieldPanel("emoji"),
        FieldPanel("meta"),
        FieldPanel("impact"),
        FieldPanel("who"),
        FieldPanel("how"),
        FieldPanel("outcome"),
        FieldPanel("quote"),
        FieldPanel("quote_author"),
        FieldPanel("portal"),
    ]

    settings_panels = [
        FieldPanel("created"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Content")),
        ObjectList(settings_panels, heading=_("Settings")),
    ])
    
    class Meta: # type: ignore
        ordering = ["title"]
        verbose_name = _("Story Item")
        verbose_name_plural = _("Story Items")

    def __str__(self):
        return self.title or _("Untitled Story")


class StoriesNotificationEmail(models.Model):
    """Model representing an email submission from the Stories page."""
    email = models.EmailField(
        verbose_name="Email",
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        help_text=_("Email address submitted from the Stories page (email)")
    )
    created = models.DateTimeField(
        verbose_name=_("Submitted"),
        auto_now_add=True,
        help_text=_("Date and time when the email was submitted (created)")
    )
    subscribed = models.BooleanField(
        default=False,
        help_text=_("Whether the email is subscribed to notifications (subscribed)")
    )
    
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.email
