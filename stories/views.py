import json
import logging
import smtplib

from contact.decorators import verify_recaptcha_token
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import StoriesNotificationEmail, StoriesRecipientsEmail, StorySubmission

logger = logging.getLogger("error_logger")

STORY_SUBMISSION_RECIPIENTS = [
    "comms@ckan.org",
]

def get_story_submission_recipients():
    """Returns a list of email addresses to which story submissions should be sent."""
    recipients = StoriesRecipientsEmail.objects.values_list("email", flat=True)
    return list(recipients) if recipients else STORY_SUBMISSION_RECIPIENTS


def _captcha_error(payload):
    """Return a 400 response when the reCAPTCHA token is missing/invalid."""
    if verify_recaptcha_token(payload.get("g-recaptcha-response")):
        return None
    return JsonResponse({"ok": False, "error": "Captcha verification failed"}, status=400)


@require_POST
def subscribe_story_notifications(request):
    """Handles subscription requests for story notifications."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid payload"}, status=400)

    captcha_error = _captcha_error(payload)
    if captcha_error is not None:
        return captcha_error

    email = (payload.get("email") or "").strip().lower()
    if not email:
        return JsonResponse({"ok": False, "error": "Email is required"}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"ok": False, "error": "Invalid email"}, status=400)

    _, created = StoriesNotificationEmail.objects.get_or_create(email=email)
    return JsonResponse({"ok": True, "created": created})


@require_POST
def submit_story(request):
    """Handles story submission requests."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid payload"}, status=400)

    captcha_error = _captcha_error(payload)
    if captcha_error is not None:
        return captcha_error

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
            fail_silently=False,
        )
    except (smtplib.SMTPException, OSError, DatabaseError):
        logger.exception(
            "Failed to send story submission notification for submission %s",
            submission.pk,
        )

    return JsonResponse({"ok": True})
