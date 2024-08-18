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
from wagtail.admin.widgets.slug import SlugInput
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable

from wagtailmetadata.models import MetadataPageMixin

from blog.models import BlogListingPage
from blog.blocks import ImageWithCaption


COMMON_PANELS = (
    FieldPanel("slug", widget=SlugInput),
    FieldPanel("seo_title"),
    FieldPanel("search_description"),
    FieldPanel("search_image"),
)


class EventPageSpeaker(Orderable):
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
    template = "events/event_list.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["events.EventPostPage"]
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        _now = now()
        recently = datetime.datetime.now().date() - datetime.timedelta(days=183)
        present = datetime.datetime.now().date()
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        html_calendar = calendar.HTMLCalendar(firstweekday=-1)
        html_calendar.cssclasses = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        all_events = EventPostPage.objects.live().public().order_by("start_date")

        featured_events = (
            EventPostPage.objects.live()
            .public()
            .filter(featured=True)
            .order_by("-created")
        )
        featured_events = list(filter(lambda x: x.start_date > _now, featured_events))

        if all_events:
            upcoming_events = list(filter(lambda x: x.start_date > _now, all_events))
            featured_event = None

            if featured_events:
                featured_event = featured_events[0]
            elif upcoming_events:
                featured_event = upcoming_events[0]

            if featured_event in upcoming_events:
                upcoming_events.remove(featured_event)

            if featured_event:
                context["featured_event_start_date"] = featured_event \
                    .start_date.strftime("%d %B %Y - %H:%M")

            all_events = (
                all_events.exclude(id__in=[featured_event.id,])
                if featured_event else all_events
            )

            all_events = all_events.order_by("-start_date")
            past_events = list(filter(lambda x: x.start_date.date() < recently, all_events))
            recent_events = list(filter(lambda x: x.start_date.date() < present and x.start_date.date() > recently, all_events))
            current_month_events = list(filter(lambda x: x.start_date.strftime("%Y-%m") == _now.strftime("%Y-%m"), all_events.order_by("start_date")))

            paginator = Paginator(past_events, 8)
            page = request.GET.get("page")
            try:
                all_past_events = paginator.page(page)
            except PageNotAnInteger:
                all_past_events = paginator.page(1)
            except EmptyPage:
                all_past_events = paginator.page(paginator.num_pages)

            context["featured_event"] = featured_event
            context["featured_events"] = featured_events
            context["upcoming_events"] = upcoming_events
            context["recent_events"] = recent_events
            context["past_events"] = all_past_events
            context["current_month_events"] = current_month_events
            context["events"] = all_events
            context["html_calendar"] = html_calendar.formatmonth(current_year, current_month, withyear=True)
        else:
            context["html_calendar"] = html_calendar.formatmonth(current_year, current_month, withyear=True)
            context["events"] = []
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
            ('event_info', blocks.StructBlock([
                ('overview', blocks.RichTextBlock(required=False)),
                ('community_activities', blocks.RichTextBlock(required=False)),
                ('highlights', blocks.RichTextBlock(required=False)),
                ('why_attend', blocks.RichTextBlock(required=False)),
                ('language', blocks.CharBlock(required=False)),
                ('joining_info', blocks.RichTextBlock(required=False)),
                ('agenda', blocks.RichTextBlock(required=False)),
                ('show_speakers', blocks.BooleanBlock(required=False)),
                ('stay_connected', blocks.RichTextBlock(required=False)),
            ], icon='list-ul')),
            ('event_video_sessions', blocks.ListBlock(blocks.StructBlock([
                ('time_start', blocks.DateTimeBlock(required=False)),
                ('time_end', blocks.DateTimeBlock(required=False)),
                ('title', blocks.CharBlock(required=False)),
                ('description', blocks.RichTextBlock(required=False)),
                ('speakers', blocks.RichTextBlock(
                    required=False,
                    help_text=_("Use a numbered or bulleted list feature to point out the speakers' names")
                )),
                ('video_link', blocks.URLBlock(required=False)),
            ]), icon='media')),
            ('event_resources', blocks.ListBlock(blocks.StructBlock([
                ('resource', DocumentChooserBlock(required=False)),
            ]), icon='doc-full-inverse')),
        ],
        null=True,
        blank=True,
        use_json_field=True,
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
        FieldPanel("content_type"),
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
