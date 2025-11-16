import calendar
import datetime

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    TabbedInterface,
    ObjectList,
    InlinePanel,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable

from wagtailmetadata.models import MetadataPageMixin

from blog.models import BlogListingPage
from blog.blocks import ImageWithCaption


COMMON_PANELS = (
    FieldPanel("slug"),
    FieldPanel("seo_title"),
    FieldPanel("search_description"),
    FieldPanel("search_image"),
)


class EventPageSpeaker(Orderable):
    """
    Represents a speaker for an event page, allowing ordering of speakers.
    Attributes:
        page (ParentalKey): Reference to the associated EventPostPage.
        first_name (str): The speaker's first name.
        last_name (str): The speaker's last name.
        image (ForeignKey): Optional image of the speaker.
        position (str): The speaker's position or title.
        info (str): Additional information about the speaker.
    Class Attributes:
        api_fields (tuple): Fields exposed via the API.
        panels (list): Wagtail admin panels for editing speaker details.
    """
    page = ParentalKey(
        "EventPostPage",
        related_name="speakers",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    first_name = models.CharField(_("Name"), max_length=255, blank=True)
    last_name = models.CharField(_("Surname"), max_length=255, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    position = models.CharField(_("Position"), max_length=255, blank=True)
    info = models.CharField(_("Additional info"), blank=True)

    api_fields = (
        "first_name",
        "last_name",
        "image",
        "position",
        "info",
    )

    panels = [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("image"),
        FieldPanel("position"),
        FieldPanel("info"),
    ]


class EventListingPage(BlogListingPage):
    """
    EventListingPage is a specialized listing page for events.
    Attributes:
        template (str): Path to the template used for rendering the event listing.
        parent_page_types (list): Allowed parent page types for this page.
        subpage_types (list): Allowed subpage types that can be created under this page.
        max_count (int): Maximum number of EventListingPage instances allowed.
    Methods:
        get_context(request, *args, **kwargs):
            Extends the context for rendering the event listing page.
            - Retrieves all live and public events, orders them by start date.
            - Filters events into featured, upcoming, recent, archived month categories.
            - Paginates archived events.
            - Generates an HTML calendar for the current month.
            - Adds all relevant event lists and calendar to the context.
    """
    template = "events/event_list.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["events.EventPostPage"]
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        _now = now()
        recently = datetime.datetime.now().date() - datetime.timedelta(days=183)
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        html_calendar = calendar.HTMLCalendar(firstweekday=-1)
        html_calendar.cssclasses = [
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        ]
        all_events = EventPostPage.objects.live().public().order_by("start_date")

        featured_events = (
            EventPostPage.objects.live()
            .public()
            .filter(featured=True)
            .order_by("-start_date")
        )

        if all_events:
            archive_events = list(filter(
                lambda x: x.start_date.date() < recently,
                all_events.order_by("-start_date")
            ))
            recent_events = list(filter(
                lambda x: x.start_date < _now and x.start_date.date() > recently,
                all_events.order_by("-start_date")
            ))
            upcoming_events = list(filter(
                lambda x: x.start_date > _now,
                all_events
            ))
            current_month_events = list(filter(
                lambda x: x.start_date.strftime("%Y-%m") == _now.strftime("%Y-%m"),
                all_events
            ))

            paginator = Paginator(archive_events, 8)
            page = request.GET.get("page")
            try:
                all_archive_events = paginator.page(page)
            except PageNotAnInteger:
                all_archive_events = paginator.page(1)
            except EmptyPage:
                all_archive_events = paginator.page(paginator.num_pages)

            context["featured_events"] = featured_events
            context["upcoming_events"] = upcoming_events
            context["recent_events"] = recent_events
            context["past_events"] = all_archive_events
            context["current_month_events"] = current_month_events
            context["events"] = all_events
            context["html_calendar"] = html_calendar.formatmonth(
                current_year, current_month, withyear=True
            )
        else:
            context["html_calendar"] = html_calendar.formatmonth(
                current_year, current_month, withyear=True
            )
            context["events"] = []
        return context


class EventPageForm(WagtailAdminPageForm):
    """
    A custom Wagtail admin form for event pages.

    This form validates the relationship between start and end dates.
    Methods
    -------
    clean():
        Ensures that the 'end_date' is not earlier than the 'start_date'.
        Adds a validation error to 'end_date' if this condition is not met.
    """
    def clean(self):
        cleaned_data = super(EventPageForm, self).clean()
        start_date = cleaned_data["start_date"]
        end_date = cleaned_data["end_date"]
        if start_date and end_date and start_date > end_date:
            self.add_error("end_date", "The end date must be after the start date")

        return cleaned_data


class EventPostPage(MetadataPageMixin, Page):
    """
    EventPostPage represents a detailed event page within the CKAN.org site.

    This model extends MetadataPageMixin and Wagtail's Page, providing fields and panels
    for configuring event details, such as title, subtitle, images, video session URL,
    event type, featured status, start/end dates, body content, and attendee count.
    It supports rich content via StreamField, including HTML, rich text, images with
    captions, event info, video sessions, and resources.
    Attributes:
        template (str): Path to the template used for rendering the event details page.
        parent_page_types (list): Allowed parent page types for this page.
        subpage_types (list): Allowed subpage types under this page.
        base_form_class (Form): Form class used for editing this page.
        EVENT_TYPE_CHOICES (list): Choices for the event type field.
        main_image (ForeignKey): Reference to the main image for the event.
        video (URLField): URL for the event's video session.
        created (DateTimeField): Timestamp when the event was created.
        post_title (CharField): Title of the event.
        event_type (CharField): Type of the event (e.g., Webinar, Conference).
        featured (BooleanField): Indicates if the event is featured.
        start_date (DateTimeField): Start date and time of the event.
        end_date (DateTimeField): End date and time of the event.
        post_subtitle (CharField): Subtitle of the event.
        body (StreamField): Rich content describing the event, including agenda, speakers, resources, etc.
        attendies (IntegerField): Number of attendees for the event.
    Panels:
        promote_panels: Panels for common page configuration.
        content_panels: Panels for editing event content.
        settings_panels: Panels for page settings.
    Methods:
        get_context(request, *args, **kwargs): Adds formatted start_date to the template context.
        get_event_duration(): Returns the event duration in minutes if end_date is set.
        get_event_status(): Returns "upcoming" if the event's start_date is in the future.
    """
    template = "events/event_details.html"
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
        help_text=_("Image"),
        on_delete=models.SET_NULL,
    )

    video = models.URLField(
        help_text=_("Video session URL"),
        blank=True,
    )

    created = models.DateTimeField(
        blank=True,
        default=now,
    )

    post_title = models.CharField(
        verbose_name=_("Event title"), max_length=512, null=False, blank=False
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
        verbose_name=_("Event subtitle"),
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
            ("event_info", blocks.StructBlock([
                ("overview", blocks.RichTextBlock(required=False)),
                ("community_activities", blocks.RichTextBlock(required=False)),
                ("highlights", blocks.RichTextBlock(required=False)),
                ("why_attend", blocks.RichTextBlock(required=False)),
                ("language", blocks.CharBlock(required=False)),
                ("joining_info", blocks.RichTextBlock(required=False)),
                ("agenda", blocks.RichTextBlock(required=False)),
                ("show_speakers", blocks.BooleanBlock(required=False)),
                ("stay_connected", blocks.RichTextBlock(required=False)),
            ], icon="list-ul")),
            ("event_video_sessions", blocks.ListBlock(blocks.StructBlock([
                ("time_start", blocks.DateTimeBlock(required=False)),
                ("time_end", blocks.DateTimeBlock(required=False)),
                ("title", blocks.CharBlock(required=False)),
                ("description", blocks.RichTextBlock(required=False)),
                ("speakers", blocks.RichTextBlock(
                    required=False,
                    help_text=_("Use a numbered or bulleted list feature to point out the speakers' names")
                )),
                ("video_link", blocks.URLBlock(required=False)),
            ]), icon="media")),
            ("event_resources", blocks.ListBlock(blocks.StructBlock([
                ("resource", DocumentChooserBlock(required=False)),
            ]), icon="doc-full-inverse")),
        ],
        null=True,
        blank=True,
    )

    attendies = models.IntegerField(
        verbose_name=_("Attendies"),
        help_text=_("Number of event's visitors"),
        null=True,
        blank=True
    )

    promote_panels = [
        MultiFieldPanel(COMMON_PANELS, heading=_("Common page configuration")),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("post_title"),
        FieldPanel("post_subtitle"),
        FieldPanel("main_image"),
        FieldPanel("video"),
        FieldPanel("event_type"),
        FieldPanel("featured", widget=forms.CheckboxInput),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("body"),
        InlinePanel("speakers", heading="Speakers", label="Speaker"),
        FieldPanel("attendies"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("id", read_only=True),
        FieldPanel("live", read_only=True),
        FieldPanel("owner"),
        FieldPanel("locked", read_only=True),
        FieldPanel("first_published_at", read_only=True),
        FieldPanel("last_published_at", read_only=True),
        FieldPanel("latest_revision_created_at", read_only=True),
        FieldPanel("show_in_menus"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(promote_panels, heading=_("Promote")),
            ObjectList(settings_panels, heading=_("Settings")),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["start_date"] = self.start_date.strftime("%d %B %Y - %H:%M")
        return context

    def get_event_duration(self):
        if self.end_date and self.start_date:
            duration = self.end_date - self.start_date
            return duration.seconds // 60
        return

    def get_event_status(self):
        if self.start_date > now():
            return "upcoming"
        return
