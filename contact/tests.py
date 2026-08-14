from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase

from contact.models import ContactPage, parse_contact_form


class ParseContactFormTests(SimpleTestCase):
    def add_session_to_request(self, request):
        middleware = SessionMiddleware(lambda req: HttpResponse())
        middleware.process_request(request)
        request.session.save()

    def test_ignores_lines_without_a_delimiter(self):
        message = "Name: Ada Lovelace\nBroken line\nEmail: ada@example.com"

        fields = parse_contact_form(message)

        self.assertEqual(fields["name"], "Ada Lovelace")
        self.assertEqual(fields["email"], "ada@example.com")
        self.assertNotIn("broken line", fields)

    def test_500_template_renders_without_request_specific_context(self):
        html = render_to_string("500.html")

        self.assertIn("Internal server error", html)

    @patch("contact.models.redirect")
    @patch("contact.models.Page.objects.filter")
    @patch("contact.models.Message.objects.get")
    @patch("contact.models.Email.objects.create")
    @patch("contact.models.send_contact_info")
    @patch("contact.models.validate_captcha", return_value=True)
    def test_serve_redirects_to_source_page_after_valid_submit(
        self,
        _mock_captcha,
        _mock_send_contact_info,
        _mock_email_create,
        mock_message_get,
        mock_page_filter,
        mock_redirect,
    ):
        page = ContactPage()
        page.form_name = "Contact Form"

        fake_form = SimpleNamespace(
            is_valid=lambda: True,
            cleaned_data={
                "how_you_heard_about_us": "Other",
                "your_e_mail_address": "user@example.com",
                "your_name": "Ada Lovelace",
                "your_phone_number": "123",
                "your_companyorganization_name": "ACME",
            },
        )

        with patch.object(page, "get_form", return_value=fake_form), patch.object(
            page, "process_form_submission", return_value=SimpleNamespace()
        ):
            request = RequestFactory().post("/", {"source-page-id": "12"})
            request.user = AnonymousUser()
            self.add_session_to_request(request)

            mock_message_get.return_value = SimpleNamespace(content="Thanks!")
            mock_page_filter.return_value.first.return_value = SimpleNamespace(url="/contact/")
            mock_redirect.return_value = SimpleNamespace(status_code=302)

            page.serve(request)

        mock_redirect.assert_called_once_with("/contact/", permanent=False)
        assert request.session["form_page_success"] is True
