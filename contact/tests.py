import hashlib
import uuid
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from wagtail.models import Page

from contact.models import (
    CkanOrgSettings,
    ContactPage,
    Email,
    MailChimpSettings,
    parse_contact_form,
    send_contact_info,
)
from contact.templatetags.modal_tags import form_modal
from contact.token import user_activation_token


class ParseContactFormTests(TestCase):
    def add_session_to_request(self, request):
        SessionMiddleware(lambda req: HttpResponse()).process_request(request)
        request.session.save()

        request._messages = FallbackStorage(request)

    def test_ignores_lines_without_a_delimiter(self):
        message = "Name: Ada Lovelace\nBroken line\nEmail: ada@example.com"

        fields = parse_contact_form(message)

        self.assertEqual(fields["name"], "Ada Lovelace")
        self.assertEqual(fields["email"], "ada@example.com")
        self.assertNotIn("broken line", fields)

    def test_ignores_blank_lines_and_keeps_nested_colons_in_value(self):
        message = (
            "Name: Ada Lovelace\n"
            "\n"
            "Details: Value with a colon: still part of the value\n"
            "Email: ada@example.com\n"
        )

        fields = parse_contact_form(message)

        self.assertEqual(fields["name"], "Ada Lovelace")
        self.assertEqual(
            fields["details"],
            "Value with a colon: still part of the value",
        )
        self.assertEqual(fields["email"], "ada@example.com")

    def test_500_template_renders_without_request_specific_context(self):
        html = render_to_string("500.html")

        self.assertIn("Internal server error", html)


class MailchimpIntegrationTests(TestCase):
    @patch("contact.models.MailchimpMarketing.Client")
    @patch.object(MailChimpSettings, "for_request")
    def test_mailchimp_integration(self, mock_for_request, mock_client_class):
        mock_for_request.return_value = SimpleNamespace(
            api_key="abc-us1",
            audience_id="list-123",
        )
        mock_client = mock_client_class.return_value

        member_info = {
            "email_address": "User@Example.com",
            "status": "subscribed",
            "merge_fields": {"FNAME": "User"},
        }

        send_contact_info(SimpleNamespace(), member_info, tags=["newsletter", "partner"])

        expected_hash = hashlib.md5(b"user@example.com").hexdigest()
        expected_body = {
            **member_info,
            "tags": [
                {"name": "newsletter", "status": "active"},
                {"name": "partner", "status": "active"},
            ],
        }
        mock_client.set_config.assert_called_once_with(
            {"api_key": "abc-us1", "server": "us1"}
        )
        mock_client.lists.set_list_member.assert_called_once_with(
            "list-123",
            expected_hash,
            expected_body,
        )

    @patch("contact.models.MailchimpMarketing.Client")
    @patch.object(MailChimpSettings, "for_request")
    def test_mailchimp_integration_skips_when_settings_missing(
        self,
        mock_for_request,
        mock_client_class,
    ):
        mock_for_request.return_value = SimpleNamespace(api_key="", audience_id="")

        send_contact_info(
            SimpleNamespace(),
            {
                "email_address": "user@example.com",
                "status": "subscribed",
                "merge_fields": {"FNAME": "User"},
            },
        )

        mock_client_class.assert_not_called()


class FormModalTagTests(TestCase):
    """Tests for the ``form_modal`` inclusion tag.

    Regression coverage for a bug where ``ContactPage.objects.get(form_name=...)``
    raised ``DoesNotExist`` (no matching page) or ``MultipleObjectsReturned``
    (duplicate ``form_name`` rows) while rendering a page, taking down the whole
    page with a 500 instead of simply omitting the modal.
    """

    def setUp(self):
        self.factory = RequestFactory()
        # Root/homepage/site are seeded by wagtailcore's initial-data migration.
        self.home = Page.objects.get(slug="home")

    def make_request(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        return request

    def make_contact_page(self, title, form_name):
        page = ContactPage(
            title=title,
            slug=uuid.uuid4().hex,
            form_name=form_name,
        )
        self.home.add_child(instance=page)
        return page

    def test_returns_context_unchanged_when_request_missing(self):
        context = {}

        result = form_modal(context)

        self.assertIs(result, context)
        self.assertNotIn("form_page", context)
        self.assertNotIn("form", context)

    @patch.object(CkanOrgSettings, "for_request")
    def test_settings_path_omits_modal_when_no_page_configured(self, mock_for_request):
        mock_for_request.return_value = SimpleNamespace(modal_form_page=None)
        context = {"request": self.make_request()}

        result = form_modal(context)

        self.assertIs(result, context)
        self.assertNotIn("form_page", context)
        self.assertNotIn("form", context)

    @patch.object(CkanOrgSettings, "for_request")
    def test_settings_path_renders_configured_modal_page(self, mock_for_request):
        page = self.make_contact_page("Contact us", "")
        mock_for_request.return_value = SimpleNamespace(modal_form_page=page)
        context = {"request": self.make_request()}

        result = form_modal(context)

        self.assertIs(result, context)
        self.assertEqual(context["form_page"], page)
        self.assertIn("form", context)
        self.assertTrue(context["form_id"])
        self.assertTrue(context["recaptcha_sitekey"])

    def test_named_form_with_no_matching_page_does_not_raise(self):
        # Regression: previously raised ContactPage.DoesNotExist -> 500.
        context = {"request": self.make_request()}

        result = form_modal(context, form_name="Webinar Form")

        self.assertIs(result, context)
        self.assertNotIn("form_page", context)
        self.assertNotIn("form", context)

    def test_named_form_with_single_match_renders_that_page(self):
        page = self.make_contact_page("Webinar", "Webinar Form")
        context = {"request": self.make_request()}

        result = form_modal(context, form_name="Webinar Form")

        self.assertIs(result, context)
        self.assertEqual(context["form_page"], page)
        self.assertIn("form", context)
        self.assertTrue(context["form_id"])

    def test_named_form_with_duplicate_names_does_not_raise(self):
        # Regression: previously raised MultipleObjectsReturned -> 500.
        first = self.make_contact_page("Webinar one", "Webinar Form")
        second = self.make_contact_page("Webinar two", "Webinar Form")
        context = {"request": self.make_request()}

        result = form_modal(context, form_name="Webinar Form")

        self.assertIs(result, context)
        self.assertIn(context["form_page"], (first, second))

    def test_missing_form_modal_renders_no_markup(self):
        # End-to-end: rendering the tag for a missing form must not raise and
        # must not emit modal markup.
        template = Template(
            "{% load modal_tags %}{% form_modal form_name='Missing Form' %}"
        )

        html = template.render(Context({"request": self.make_request()}))

        self.assertNotIn("micromodal", html)
        self.assertNotIn("modal-link", html)


class NewsletterSubscriptionTests(TestCase):
    """Anti-spam and SES best-practice coverage for the newsletter signup.

    The confirmation email ("You're Almost In...") was being sent to arbitrary
    addresses because the AJAX endpoint never validated the invisible reCAPTCHA
    token, and unconfirmed addresses were pushed into Mailchimp immediately.
    """

    URL = "/ajax-posting/"

    def post(self, **overrides):
        data = {
            "form_id": "#subscribe_form",
            "name": "Ada Lovelace",
            "email": "ada@example.com",
        }
        data.update(overrides)
        return self.client.post(
            self.URL, data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

    @patch("contact.views.validate_captcha", return_value=False)
    def test_missing_captcha_is_rejected(self, mock_captcha):
        response = self.post()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Email.objects.exists())

    @patch("contact.views.validate_captcha", return_value=True)
    def test_non_ajax_request_is_rejected(self, mock_captcha):
        response = self.client.post(
            self.URL,
            {"form_id": "#subscribe_form", "name": "Ada", "email": "a@example.com"},
        )

        self.assertEqual(response.status_code, 400)
        mock_captcha.assert_not_called()

    @patch("contact.views.validate_captcha", return_value=True)
    def test_invalid_email_is_rejected(self, mock_captcha):
        response = self.post(email="not-an-email")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Email.objects.exists())

    @patch("contact.views.validate_captcha", return_value=True)
    def test_missing_name_is_rejected(self, mock_captcha):
        response = self.post(name="")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Email.objects.exists())

    @patch("contact.views.send_subscription_email")
    @patch("contact.views.validate_captcha", return_value=True)
    def test_valid_submission_sends_one_confirmation(self, mock_captcha, mock_send):
        response = self.post()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertTrue(Email.objects.filter(address="ada@example.com").exists())
        mock_send.assert_called_once()

    @patch("contact.views.send_subscription_email")
    @patch("contact.views.validate_captcha", return_value=True)
    def test_repeat_submission_is_throttled(self, mock_captcha, mock_send):
        first = self.post()
        second = self.post()

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        # Only the first request triggers a confirmation email.
        mock_send.assert_called_once()

    @patch("contact.views.send_contact_info")
    @patch("contact.views.send_subscription_email")
    @patch("contact.views.validate_captcha", return_value=True)
    def test_not_added_to_mailchimp_before_confirmation(
        self, mock_captcha, mock_send, mock_contact
    ):
        self.post()

        mock_contact.assert_not_called()

    @patch("contact.views.send_contact_info")
    def test_activation_confirms_and_adds_to_mailchimp(self, mock_contact):
        subscriber = Email.objects.create(
            form_name="Subscribe Form",
            full_name="Ada Lovelace",
            address="ada@example.com",
        )
        eid = urlsafe_base64_encode(force_bytes(subscriber.address))
        token = user_activation_token.make_token(subscriber.address)

        response = self.client.get(
            f"/newsletter/subscription/activate/{eid}/{token}"
        )

        self.assertEqual(response.status_code, 302)
        subscriber.refresh_from_db()
        self.assertTrue(subscriber.subscribed)
        mock_contact.assert_called_once()
