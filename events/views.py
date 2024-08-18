import calendar
import datetime
import json

from django.http import HttpResponse
from django.views.generic.detail import DetailView

from wagtail.log_actions import log
from wagtail.snippets.views.snippets import CreateView

from .models import EventListingPage, EventPostPage


class EventCreateView(CreateView):
    def save_instance(self):
        """
        Called after the form is successfully validated - saves the object to the db
        and returns the new object.
        """
        parent = EventListingPage.objects.first()

        if self.draftstate_enabled:
            instance = self.form.save(commit=False)

            if not instance.owner:
                instance.owner = self.request.user

            # If DraftStateMixin is applied, only save to the database in CreateView,
            # and make sure the live field is set to False.
            if self.view_name == "create":
                instance.live = False
                parent.add_child(instance=instance)
                self.form.save_m2m()
        else:
            instance = self.form.save()

        self.has_content_changes = self.view_name == "create" or self.form.has_changed()

        # Save revision if the model inherits from RevisionMixin
        self.new_revision = None
        if self.revision_enabled:
            self.new_revision = instance.save_revision(user=self.request.user)

        log(
            instance=instance,
            action="wagtail.create" if self.view_name == "create" else "wagtail.edit",
            revision=self.new_revision,
            content_changed=self.has_content_changes,
        )

        return instance


class EventVideoPageView(DetailView):
    model = EventPostPage
    template_name = "events/event_video.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timelog"] = int(self.kwargs.get("timelog"))
        return context


def get_events_data(request):
    direction = int(request.GET.get("direction"))
    month = request.GET.get("month")
    month = list(calendar.month_name).index(month)
    year = int(request.GET.get("year"))
    if month == 12 and direction == 1: 
        year = year + 1
        month = 1
        direction = 0
    if month == 1 and direction == -1:
        year = year - 1
        month = 12
        direction = 0
    next_month = month + direction
    firstweekday = datetime.datetime(year, next_month, 1, 0, 0, 0).strftime("%A")

    html_calendar = calendar.HTMLCalendar(firstweekday=-1)
    html_calendar.cssclasses = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    new_calendar = html_calendar.formatmonth(year, next_month, withyear=True)

    try:
        events = EventPostPage.objects.filter(start_date__year=year) \
            .filter(start_date__month=next_month).order_by("start_date")

    except Exception as e:
        data = f'Fail: {e}'

    events_data = []
    for event in events:
        event_data = {
            "title": event.post_title,
            "description": event.post_subtitle,
            "slug": event.slug,
            "day": str(event.start_date.day),
            "weekday": calendar.day_name[event.start_date.weekday()],
            "time": event.start_date.time().strftime("%I:%M%p")
        }
        events_data.append(event_data)

    results = {"calendar": new_calendar, "firstweekday": firstweekday, "calendar_events": events_data}
    data = json.dumps(results)

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)
