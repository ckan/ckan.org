import logging
import smtplib
import typing

from blog.models import BlogPostPage
from contact.antispam import honeypot_triggered
from contact.decorators import validate_captcha
from contact.models import Email, send_contact_info
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.response import TemplateResponse
from stories.views import get_story_submission_recipients
from wagtail.models import Page

from .forms import GetInvolvedForm

logger = logging.getLogger("error_logger")

FORM_NAME = "Get Involved Form"
CAPTCHA_ERROR = "Please complete the captcha."


def _wants_json(request) -> bool:
	"""True for the progressive-enhancement fetch() submit in anniversary.js."""
	return request.headers.get("x-requested-with") == "XMLHttpRequest"


class AnniversaryPage(Page):
	parent_page_types: typing.ClassVar[list[str]] = ["home.HomePage"]
	template = "anniversary/anniversary.html"
	max_count = 1  # Only one anniversary page

	content_panels = Page.content_panels + [
	]

	class Meta: # type: ignore
		verbose_name = "Anniversary Page"
		verbose_name_plural = "Anniversary Pages"

	def serve(self, request, *args, **kwargs):
		if request.method != "POST":
			return super().serve(request, *args, **kwargs)

		status, errors = self.process_get_involved_form(request)
		success = status == 200

		if _wants_json(request):
			return JsonResponse({"ok": success, "errors": errors}, status=status)

		# No-JS fallback: re-render the page with the result shown in place.
		context = self.get_context(request, *args, **kwargs)
		context["success"] = success
		context["form_errors"] = errors
		return TemplateResponse(request, self.get_template(request, *args, **kwargs), context)

	def process_get_involved_form(self, request):
		"""Validate and handle a "Get Involved" submission.

		Returns ``(status_code, errors)``. Bots caught by the honeypot get a
		success response so they do not retry, but nothing is stored or sent
		(same policy as the other public forms, see contact/antispam.py).
		"""
		if honeypot_triggered(request.POST):
			return 200, {}

		if not validate_captcha(request):
			return 400, {"captcha": [CAPTCHA_ERROR]}

		form = GetInvolvedForm(request.POST)
		if not form.is_valid():
			return 400, {field: list(messages) for field, messages in form.errors.items()}

		data = form.cleaned_data
		name = data["FNAME"]
		email = data["EMAIL"]

		submission = Email.objects.create(
			form_name=FORM_NAME,
			full_name=name,
			address=email,
			message=data["MESSAGE"],
		)
		send_contact_info(request, {
			"email_address": email,
			"status": "subscribed",
			"merge_fields": {
				"FNAME": name.split(" ")[0],
				"LNAME": name.split(" ")[-1],
				"FORM": FORM_NAME,
				"ORG": data["ORG"],
				"CKANUSE": data["CKANUSE"],
				"MESSAGE": data["MESSAGE"],
			},
		})
		self.notify_team(submission, data)
		return 200, {}

	def notify_team(self, submission, data):
		"""E-mail the comms team about a new submission.

		Recipients are managed in the admin (Stories recipients emails, falling
		back to comms@ckan.org). A mail failure must never lose the submission:
		it is already stored and visible under Contacts > Emails.
		"""
		body = (
			"A new message was sent from the CKAN 20th anniversary page.\n\n"
			f"Name:         {data['FNAME']}\n"
			f"Organization: {data['ORG'] or '—'}\n"
			f"Email:        {data['EMAIL']}\n"
			f"Relationship: {data['CKANUSE'] or '—'}\n\n"
			f"Message:\n{data['MESSAGE'] or '—'}\n\n"
			f"Submitted: {submission.submitted:%Y-%m-%d %H:%M} UTC\n"
		)
		try:
			send_mail(
				subject=f"New anniversary message — {data['ORG'] or data['FNAME']}",
				message=body,
				from_email=settings.DEFAULT_FROM_EMAIL,
				recipient_list=get_story_submission_recipients(),
				fail_silently=False,
			)
		except (smtplib.SMTPException, OSError):
			logger.exception("Failed to send anniversary form notification for Email %s", submission.pk)

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		context["form"] = GetInvolvedForm()
		# Stories
		last_year_posts = BlogPostPage.objects.filter(is_story=True)
		context["stories"] = last_year_posts.order_by("story_publish_date")
		# Recaptcha
		context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
		return context
