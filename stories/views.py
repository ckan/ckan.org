import json
import logging

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from contact.models import MailChimpSettings
from .models import StoriesNotificationEmail, StoriesRecipientsEmail, StorySubmission

STORY_SUBMISSION_RECIPIENTS = [
    "comms@ckan.org",
]

logger = logging.getLogger(__name__)


def get_story_submission_recipients():
    """Returns a list of email addresses to which story submissions should be sent."""
    recipients = StoriesRecipientsEmail.objects.values_list("email", flat=True)
    return list(recipients) if recipients else STORY_SUBMISSION_RECIPIENTS


def _sync_to_mailchimp(request, email):
    mc = MailChimpSettings.for_request(request)
    api_key = mc.api_key
    audience_id = mc.stories_audience_id

    if not api_key or not audience_id:
        logger.warning("Mailchimp stories audience not configured — skipping subscriber sync")
        return

    try:
        client = MailchimpMarketing.Client()
        client.set_config({"api_key": api_key, "server": api_key.split("-")[-1]})
        client.lists.add_list_member(audience_id, {"email_address": email, "status": "subscribed"})
    except ApiClientError as error:
        if error.status_code == 400 and "is already a list member" in error.text:
            return
        logger.error("Mailchimp sync failed for %s: %s", email, error.text)
    except Exception:
        logger.exception("Mailchimp sync failed for %s", email)


@require_POST
def subscribe_story_notifications(request):
    """Handles subscription requests for story notifications."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid payload"}, status=400)

    email = (payload.get("email") or "").strip().lower()
    if not email:
        return JsonResponse({"ok": False, "error": "Email is required"}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"ok": False, "error": "Invalid email"}, status=400)

    obj, created = StoriesNotificationEmail.objects.get_or_create(email=email)
    _sync_to_mailchimp(request, email)
    return JsonResponse({"ok": True, "created": created})


@require_POST
def submit_story(request):
    """Handles story submission requests."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid payload"}, status=400)

    email = (payload.get("email") or "").strip().lower()
    if not email:
        return JsonResponse({"ok": False, "error": "Email is required"}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"ok": False, "error": "Invalid email"}, status=400)

    name = (payload.get("name") or "").strip()
    org = (payload.get("org") or "").strip()
    portal_url = (payload.get("portal_url") or "").strip()
    message = (payload.get("message") or "").strip()

    submission = StorySubmission.objects.create(
        name=name,
        org=org,
        email=email,
        portal_url=portal_url,
        message=message,
    )

    subject = f"New CKAN story submission — {org or name or email}"
    body = (
        f"A new story submission was received.\n\n"
        f"Name:       {name or '—'}\n"
        f"Org:        {org or '—'}\n"
        f"Email:      {email}\n"
        f"Portal URL: {portal_url or '—'}\n\n"
        f"Message:\n{message or '—'}\n\n"
        f"View in admin: https://ckan.org/admin/snippets/stories/storysubmission/edit/{submission.pk}/\n"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=get_story_submission_recipients(),
            fail_silently=True,
        )
    except Exception:
        pass

    return JsonResponse({"ok": True})
