import re
from datetime import date

from django.test import TestCase
from stories.models import StoriesPage
from wagtail.models import Page

from ckan_pages.models import PrivacyPolicyPage


class PrivacyPolicyTests(TestCase):
    """Privacy Policy page and footer links (#358)."""

    def setUp(self):
        self.home = Page.objects.get(slug="home")
        # Any page that uses the site footer.
        self.other = self.home.add_child(instance=StoriesPage(title="Success stories", slug="success-stories"))

    def add_policy(self):
        return self.home.add_child(instance=PrivacyPolicyPage(
            title="Privacy Policy", slug="privacy-policy", last_updated=date(2026, 11, 6)))

    def footer(self):
        html = self.client.get(self.other.url).content.decode()
        return html[html.index("<footer"):]

    def test_footer_has_no_broken_links_before_the_page_exists(self):
        html = self.footer()

        self.assertNotIn('href="None"', html)
        self.assertIn("in accordance with our privacy policy", html)
        self.assertNotIn('class="footer-legal-links"', html)

    def test_footer_links_to_the_policy_once_published(self):
        policy = self.add_policy()

        html = self.footer()

        self.assertEqual(len(re.findall(rf'href="{re.escape(policy.url)}"', html)), 2)
        self.assertIn('class="footer-legal-links"', html)

    def test_policy_describes_the_analytics_actually_in_use(self):
        response = self.client.get(self.add_policy().url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google Analytics 4")
        self.assertContains(response, "<strong>_ga</strong>", html=False)
        self.assertNotContains(response, "Plausible")
        self.assertContains(response, "6 November 2026")
