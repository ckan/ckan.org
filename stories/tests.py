import hashlib
import json
from io import StringIO
from unittest.mock import patch

import requests
from contact.models import MailChimpSettings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from mailchimp_marketing.api_client import ApiClientError
from wagtail.models import Page, Site

from stories.models import StoriesNotificationEmail, StoriesPage, StorySubmission

CAPTCHA_PATCH = "stories.views.verify_recaptcha_token"


class StoriesAntiSpamTests(TestCase):
    """The custom success-stories forms must not be submittable without a
    valid reCAPTCHA token."""

    SUBMIT_URL = "/success-stories/submit/"
    NOTIFY_URL = "/success-stories/notify/subscribe/"

    def post_json(self, url, payload):
        return self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )

    @patch(CAPTCHA_PATCH, return_value=False)
    def test_submit_story_requires_captcha(self, mock_verify):
        response = self.post_json(self.SUBMIT_URL, {"email": "ada@example.com"})

        self.assertEqual(response.status_code, 400)
        self.assertFalse(StorySubmission.objects.exists())

    @patch(CAPTCHA_PATCH, return_value=False)
    def test_notify_requires_captcha(self, mock_verify):
        response = self.post_json(self.NOTIFY_URL, {"email": "ada@example.com"})

        self.assertEqual(response.status_code, 400)
        self.assertFalse(StoriesNotificationEmail.objects.exists())

    @patch("stories.views.send_mail")
    @patch(CAPTCHA_PATCH, return_value=True)
    def test_submit_story_with_captcha_succeeds(self, mock_verify, mock_mail):
        response = self.post_json(
            self.SUBMIT_URL,
            {
                "email": "ada@example.com",
                "name": "Ada Lovelace",
                "message": "A great CKAN portal",
                "g-recaptcha-response": "token",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertTrue(StorySubmission.objects.exists())
        mock_mail.assert_called_once()

    @patch(CAPTCHA_PATCH, return_value=True)
    def test_notify_with_captcha_succeeds(self, mock_verify):
        response = self.post_json(
            self.NOTIFY_URL,
            {"email": "ada@example.com", "g-recaptcha-response": "token"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertTrue(
            StoriesNotificationEmail.objects.filter(
                email="ada@example.com"
            ).exists()
        )


MAILCHIMP_CLIENT = "stories.mailchimp.MailchimpMarketing.Client"


def configure_mailchimp(api_key="key-us21", stories_audience_id="stories123", audience_id="news456"):
    mailchimp_settings = MailChimpSettings.for_site(Site.objects.get(is_default_site=True))
    mailchimp_settings.api_key = api_key
    mailchimp_settings.audience_id = audience_id
    mailchimp_settings.stories_audience_id = stories_audience_id
    mailchimp_settings.save()


@patch(CAPTCHA_PATCH, return_value=True)
@patch(MAILCHIMP_CLIENT)
class StoryNotificationMailchimpTests(TestCase):
    """Story notification sign-ups are synced to their own Mailchimp audience (#356)."""

    NOTIFY_URL = "/success-stories/notify/subscribe/"

    def subscribe(self, email="Ada@Example.com"):
        return self.client.post(
            self.NOTIFY_URL,
            data=json.dumps({"email": email, "g-recaptcha-response": "token"}),
            content_type="application/json",
        )

    def test_signup_is_added_to_stories_audience_as_pending(self, mock_client, _captcha):
        configure_mailchimp()

        response = self.subscribe()

        self.assertEqual(response.status_code, 200)
        client = mock_client.return_value
        client.set_config.assert_called_once_with({"api_key": "key-us21", "server": "us21"})
        audience_id, subscriber_hash, body = client.lists.set_list_member.call_args.args
        self.assertEqual(audience_id, "stories123")  # never the newsletter audience
        self.assertEqual(subscriber_hash, hashlib.md5(b"ada@example.com").hexdigest())
        # Double opt-in for new members; no "status" key, so an existing member
        # who unsubscribed is never re-subscribed.
        self.assertEqual(body, {"email_address": "ada@example.com", "status_if_new": "pending"})

    def test_not_configured_keeps_local_signup_only(self, mock_client, _captcha):
        configure_mailchimp(stories_audience_id="")

        with self.assertLogs("error_logger", level="WARNING"):
            response = self.subscribe()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(StoriesNotificationEmail.objects.exists())
        mock_client.return_value.lists.set_list_member.assert_not_called()

    def test_mailchimp_rejection_does_not_fail_the_signup(self, mock_client, _captcha):
        configure_mailchimp()
        mock_client.return_value.lists.set_list_member.side_effect = ApiClientError("Bad Request", 400)

        with self.assertLogs("error_logger", level="ERROR") as logs:
            response = self.subscribe()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertNotIn("ada@example.com", "\n".join(logs.output))  # no addresses in logs

    def test_mailchimp_unreachable_does_not_fail_the_signup(self, mock_client, _captcha):
        configure_mailchimp()
        mock_client.return_value.lists.set_list_member.side_effect = requests.ConnectionError()

        with self.assertLogs("error_logger", level="ERROR"):
            response = self.subscribe()

        self.assertEqual(response.status_code, 200)

    def test_repeat_signup_is_synced_again(self, mock_client, _captcha):
        configure_mailchimp()

        self.subscribe()
        response = self.subscribe()

        self.assertFalse(response.json()["created"])
        self.assertEqual(StoriesNotificationEmail.objects.count(), 1)
        self.assertEqual(mock_client.return_value.lists.set_list_member.call_count, 2)


@patch(MAILCHIMP_CLIENT)
class SyncStorySubscribersCommandTests(TestCase):

    def setUp(self):
        for email in ("a@example.com", "b@example.com", "c@example.com"):
            StoriesNotificationEmail.objects.create(email=email)

    def run_command(self, *args):
        out = StringIO()
        call_command("sync_story_subscribers", *args, stdout=out)
        return out.getvalue()

    def test_refuses_to_run_without_stories_audience(self, mock_client):
        configure_mailchimp(stories_audience_id="")

        with self.assertRaises(CommandError):
            self.run_command()
        mock_client.return_value.lists.set_list_member.assert_not_called()

    def test_dry_run_only_counts(self, mock_client):
        configure_mailchimp()

        output = self.run_command("--dry-run")

        self.assertIn("3 sign-up(s) would be synced", output)
        mock_client.return_value.lists.set_list_member.assert_not_called()

    def test_syncs_all_and_reports_failures(self, mock_client):
        configure_mailchimp()
        mock_client.return_value.lists.set_list_member.side_effect = [
            None, ApiClientError("Bad Request", 400), None,
        ]

        with self.assertLogs("error_logger", level="ERROR"):
            output = self.run_command()

        self.assertIn("Synced 2 of 3 sign-up(s).", output)
        self.assertIn("1 failed", output)
        synced = [c.args[2]["email_address"] for c in mock_client.return_value.lists.set_list_member.call_args_list]
        self.assertEqual(synced, ["a@example.com", "b@example.com", "c@example.com"])


class StoryNotificationCopyTests(TestCase):
    """The sign-up confirmation only asks people to check their inbox when a
    Mailchimp opt-in e-mail is actually sent."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.page = home.add_child(instance=StoriesPage(title="Success stories", slug="success-stories"))

    def test_copy_without_stories_audience(self):
        response = self.client.get(self.page.url)

        self.assertContains(response, "re on the list")
        self.assertNotContains(response, "Check your inbox")

    def test_copy_with_stories_audience(self):
        configure_mailchimp()

        response = self.client.get(self.page.url)

        self.assertContains(response, "Check your inbox")
        self.assertNotContains(response, "re on the list")
