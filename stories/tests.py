import json
from unittest.mock import patch

from django.test import TestCase

from stories.models import StoriesNotificationEmail, StorySubmission

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

