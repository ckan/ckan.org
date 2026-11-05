import re

from django.test import TestCase, override_settings
from wagtail.models import Page
from wagtail.rich_text import RichText

from stories.models import StoriesPage, StoryItem


@override_settings(WAGTAILADMIN_BASE_URL="https://ckan.org")
class StoryLinkPreviewTests(TestCase):
    """Shared ?story=<slug> links get that story's preview in the server HTML (#340)."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.page = home.add_child(instance=StoriesPage(title="Success stories", slug="success-stories"))
        self.story = StoryItem.objects.create(
            org="Humanitarian Data Exchange",
            title='Data for "crisis" response',
            slug="hdx-humanitarian-data-exchange",
            challenge=[("paragraph", RichText(
                "<p>Humanitarian <b>data</b> was scattered &amp; hard to find. " + "word " * 80 + "</p>"
            ))],
        )

    def head(self, query=""):
        response = self.client.get(self.page.url + query)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        return html[:html.index("</head>")]

    def meta(self, head, prop):
        match = re.search(rf'<meta (?:property|name)="{re.escape(prop)}" content="([^"]*)"', head)
        return match and match.group(1)

    def test_page_without_story_has_generic_preview(self):
        head = self.head()

        self.assertEqual(self.meta(head, "og:title"), "CKAN Success Stories")
        self.assertEqual(self.meta(head, "og:type"), "website")
        self.assertEqual(self.meta(head, "og:url"), "https://ckan.org/success-stories")
        self.assertEqual(self.meta(head, "og:image"), "https://ckan.org/static/img/ckan-stories-og.png")
        self.assertEqual(self.meta(head, "twitter:card"), "summary_large_image")
        self.assertIn("<title>Success Stories - CKAN</title>", head)

    def test_shared_story_link_gets_story_preview(self):
        head = self.head("?story=hdx-humanitarian-data-exchange")

        self.assertEqual(self.meta(head, "og:title"), "Humanitarian Data Exchange — Data for &quot;crisis&quot; response")
        self.assertEqual(self.meta(head, "og:type"), "article")
        self.assertEqual(self.meta(head, "og:url"), "https://ckan.org/success-stories?story=hdx-humanitarian-data-exchange")
        self.assertEqual(self.meta(head, "twitter:title"), self.meta(head, "og:title"))
        description = self.meta(head, "og:description")
        self.assertTrue(description.startswith("Humanitarian data was scattered &amp; hard to find. word"))
        self.assertLessEqual(len(description.replace("&amp;", "&")), 200)
        self.assertNotIn("<", description)
        # One canonical URL for all variants: the body is identical.
        self.assertIn('<link rel="canonical" href="https://ckan.org/success-stories">', head)

    def test_story_without_slug_is_matched_by_id_like_stories_js(self):
        StoryItem.objects.filter(pk=self.story.pk).update(slug="")

        head = self.head(f"?story={self.story.pk}")

        self.assertTrue(self.meta(head, "og:title").startswith("Humanitarian Data Exchange"))
        self.assertEqual(self.meta(head, "og:url"), f"https://ckan.org/success-stories?story={self.story.pk}")

    def test_unknown_story_falls_back_to_generic_preview(self):
        head = self.head("?story=does-not-exist")

        self.assertEqual(self.meta(head, "og:title"), "CKAN Success Stories")
        self.assertEqual(self.meta(head, "og:url"), "https://ckan.org/success-stories")

    def test_urls_are_https_even_behind_a_plain_http_proxy(self):
        head = self.head("?story=hdx-humanitarian-data-exchange")

        for prop in ("og:url", "og:image", "twitter:image"):
            self.assertTrue(self.meta(head, prop).startswith("https://ckan.org/"), prop)
