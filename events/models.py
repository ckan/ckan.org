from django import forms
from django.db import models
from django.utils.timezone import now

from wagtail.models import Page
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    TabbedInterface,
    ObjectList,
)
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.widgets.slug import SlugInput

from wagtailmetadata.models import MetadataPageMixin

from blog.models import BlogListingPage
from blog.blocks import ImageWithCaption


COMMON_PANELS = (
    FieldPanel("slug", widget=SlugInput),
    FieldPanel("seo_title"),
    FieldPanel("search_description"),
    FieldPanel("search_image"),
)


class EventListingPage(BlogListingPage):
    template = "events/event_listing_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["events.EventPostPage"]
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        _now = now()
        all_posts = EventPostPage.objects.live().public().order_by("start_date")
        featured_posts = (
            EventPostPage.objects.live()
            .public()
            .filter(featured=True)
            .order_by("-created")
        )
        featured_posts = list(filter(lambda x: x.start_date > _now, featured_posts))
        if all_posts:
            upcoming_events = list(filter(lambda x: x.start_date > _now, all_posts))
            featured_post = None
            if featured_posts:
                featured_post = featured_posts[0]
            elif upcoming_events:
                featured_post = upcoming_events[0]
            if featured_post in upcoming_events:
                upcoming_events.remove(featured_post)
            if featured_post:
                context["featured_post_start_date"] = featured_post.start_date.strftime(
                    "%d %B %Y - %H:%M"
                )
            all_posts = (
                all_posts.exclude(
                    id__in=[
                        featured_post.id,
                    ]
                )
                if featured_post
                else all_posts
            )
            all_posts = all_posts.order_by("-start_date")
            past_events = list(filter(lambda x: x.start_date < _now, all_posts))
            context["featured_post"] = featured_post
            context["posts"] = upcoming_events
            context["past_events"] = past_events[:10]
        else:
            context["posts"] = []
        return context


class EventPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super(EventPageForm, self).clean()
        start_date = cleaned_data["start_date"]
        end_date = cleaned_data["end_date"]
        if start_date and end_date and start_date > end_date:
            self.add_error("end_date", "The end date must be after the start date")

        return cleaned_data


class EventPostPage(MetadataPageMixin, Page):
    template = "events/event_post_page.html"
    parent_page_types = ["events.EventListingPage"]
    subpage_types = []
    base_form_class = EventPageForm

    EVENT_TYPE_CHOICES = [
        ("Webinar", "Webinar"),
        ("Presentation", "Presentation"),
        ("Meeting", "Meeting"),
        ("Conference", "Conference"),
        ("Other", "Other"),
    ]
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        help_text="Image",
        on_delete=models.SET_NULL,
    )
    created = models.DateTimeField(
        blank=True,
        default=now,
    )
    post_title = models.CharField(
        verbose_name="Event title", max_length=512, null=False, blank=False
    )
    event_type = models.CharField(
        max_length=32, choices=EVENT_TYPE_CHOICES, default="Webinar"
    )
    featured = models.BooleanField(null=True, default=False)
    start_date = models.DateTimeField(
        null=False,
        blank=False,
        default=now,
    )
    end_date = models.DateTimeField(null=True, blank=True)
    post_subtitle = models.CharField(
        verbose_name="Event subtitle",
        max_length=512,
        null=True,
        blank=True,
    )
    body = StreamField(
        [
            ("html", blocks.RawHTMLBlock()),
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
            ("post_image", ImageWithCaption()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading="Common page configuration"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("post_title"),
        FieldPanel("post_subtitle"),
        FieldPanel("main_image"),
        FieldPanel("event_type"),
        FieldPanel("featured", widget=forms.CheckboxInput),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("body"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("id", read_only=True),
        FieldPanel("live", read_only=True),
        FieldPanel("owner"),
        FieldPanel("content_type"),
        FieldPanel("locked", read_only=True),
        FieldPanel("first_published_at", read_only=True),
        FieldPanel("last_published_at", read_only=True),
        FieldPanel("latest_revision_created_at", read_only=True),
        FieldPanel("show_in_menus"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(promote_panels, heading="Promote"),
            ObjectList(settings_panels, heading="Settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["start_date"] = self.start_date.strftime("%d %B %Y - %H:%M")
        return context
