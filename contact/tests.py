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
from wagtail.models import Page

from contact.models import (
    CkanOrgSettings,
    ContactPage,
    MailChimpSettings,
    parse_contact_form,
    send_contact_info,
)
from contact.templatetags.modal_tags import form_modal


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
