import hashlib
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.test import TestCase

from contact.models import MailChimpSettings, parse_contact_form, send_contact_info


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
