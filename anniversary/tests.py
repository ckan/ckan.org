import smtplib
from unittest.mock import patch

from contact.models import Email
from django.core import mail
from django.test import TestCase
from stories.models import StoriesRecipientsEmail
from wagtail.models import Page

from anniversary.models import AnniversaryPage

CAPTCHA = "anniversary.models.validate_captcha"
MAILCHIMP = "anniversary.models.send_contact_info"
AJAX = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}


@patch(MAILCHIMP)
class GetInvolvedFormTests(TestCase):
    """The "Get Involved" form on the 20th anniversary page (#354)."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.page = home.add_child(instance=AnniversaryPage(title="20 years of CKAN", slug="20-years-of-ckan"))

    def form_data(self, **overrides):
        data = {
            "FNAME": "Ada Lovelace",
            "ORG": "Analytical Engines Ltd",
            "EMAIL": "ada@example.com",
            "CKANUSE": "contributor",
            "MESSAGE": "Happy birthday CKAN!",
            "website": "",  # honeypot, always submitted empty by a real browser
            "g-recaptcha-response": "token",
        }
        data.update(overrides)
        return data

    def post(self, ajax=True, **overrides):
        return self.client.post(self.page.url, self.form_data(**overrides), **(AJAX if ajax else {}))

    @patch(CAPTCHA, return_value=True)
    def test_ajax_submission_is_stored_synced_and_notified(self, _captcha, mock_mailchimp):
        response = self.post()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True, "errors": {}})

        stored = Email.objects.get()
        self.assertEqual((stored.form_name, stored.full_name, stored.address, stored.message),
                         ("Get Involved Form", "Ada Lovelace", "ada@example.com", "Happy birthday CKAN!"))

        member = mock_mailchimp.call_args.args[1]
        self.assertEqual(member["email_address"], "ada@example.com")
        self.assertEqual(member["merge_fields"]["ORG"], "Analytical Engines Ltd")
        self.assertEqual(member["merge_fields"]["CKANUSE"], "contributor")

        self.assertEqual(len(mail.outbox), 1)
        notification = mail.outbox[0]
        self.assertEqual(notification.to, ["comms@ckan.org"])  # fallback recipient
        self.assertIn("Analytical Engines Ltd", notification.subject)
        for value in ("Ada Lovelace", "ada@example.com", "contributor", "Happy birthday CKAN!"):
            self.assertIn(value, notification.body)

    @patch(CAPTCHA, return_value=True)
    def test_notification_uses_recipients_managed_in_admin(self, _captcha, _mailchimp):
        StoriesRecipientsEmail.objects.create(email="team@example.org")

        self.post()

        self.assertEqual(mail.outbox[0].to, ["team@example.org"])

    @patch(CAPTCHA, return_value=True)
    def test_same_person_can_submit_twice(self, _captcha, _mailchimp):
        self.assertEqual(self.post().status_code, 200)
        self.assertEqual(self.post(MESSAGE="One more thing").status_code, 200)

        self.assertEqual(Email.objects.count(), 2)

    @patch(CAPTCHA, return_value=False)
    def test_failed_captcha_is_rejected(self, _captcha, mock_mailchimp):
        response = self.post()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errors"], {"captcha": ["Please complete the captcha."]})
        self.assertFalse(Email.objects.exists())
        mock_mailchimp.assert_not_called()
        self.assertEqual(mail.outbox, [])

    @patch(CAPTCHA, return_value=True)
    def test_invalid_form_returns_field_errors(self, _captcha, mock_mailchimp):
        response = self.post(EMAIL="not-an-email", FNAME="")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()["errors"]), {"EMAIL", "FNAME"})
        self.assertFalse(Email.objects.exists())
        mock_mailchimp.assert_not_called()

    @patch(CAPTCHA, return_value=True)
    def test_filled_honeypot_looks_successful_but_is_dropped(self, _captcha, mock_mailchimp):
        response = self.post(website="https://spam.example")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertFalse(Email.objects.exists())
        mock_mailchimp.assert_not_called()
        self.assertEqual(mail.outbox, [])

    @patch(CAPTCHA, return_value=True)
    def test_missing_honeypot_is_dropped(self, _captcha, mock_mailchimp):
        data = self.form_data()
        data.pop("website")

        response = self.client.post(self.page.url, data, **AJAX)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Email.objects.exists())
        mock_mailchimp.assert_not_called()

    @patch("anniversary.models.send_mail", side_effect=smtplib.SMTPException("down"))
    @patch(CAPTCHA, return_value=True)
    def test_mail_failure_keeps_the_submission(self, _captcha, _send_mail, _mailchimp):
        with self.assertLogs("error_logger", level="ERROR"):
            response = self.post()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Email.objects.exists())

    @patch(CAPTCHA, return_value=True)
    def test_no_js_submission_renders_success_state(self, _captcha, _mailchimp):
        response = self.post(ajax=False)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="involve-form is-sent"')
        self.assertTrue(Email.objects.exists())

    @patch(CAPTCHA, return_value=False)
    def test_no_js_failure_renders_error_message(self, _captcha, _mailchimp):
        response = self.post(ajax=False)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "is-sent")
        self.assertContains(response, "Please complete the captcha.")

    def test_get_renders_form_with_honeypot_and_join_anchor(self, _mailchimp):
        response = self.client.get(self.page.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="join"')  # keep existing shared links working
        self.assertContains(response, 'name="website"')
        self.assertNotContains(response, "is-sent")
        self.assertContains(response, 'id="joinFormError" role="alert" hidden')
