import re

from django.test import TestCase
from wagtail.models import Page

from blog.models import BlogListingPage, BlogPostPage


class MetaDescriptionTests(TestCase):
    """Every page outputs exactly one non-empty meta description."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.blog = home.add_child(instance=BlogListingPage(title="Blog", slug="blog"))

    def add_post(self, **kwargs):
        return self.blog.add_child(instance=BlogPostPage(title="Post", post_title="Post", slug="post", **kwargs))

    def descriptions(self, page):
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        return re.findall(r'<meta name="description" content="([^"]*)"', response.content.decode())

    def test_search_description_is_the_only_description(self):
        post = self.add_post(search_description="Written by the editor.", post_subtitle="Subtitle.")
        self.assertEqual(self.descriptions(post), ["Written by the editor."])

    def test_falls_back_to_subtitle(self):
        post = self.add_post(post_subtitle="What the post is about.")
        self.assertEqual(self.descriptions(post), ["What the post is about."])

    def test_falls_back_to_title_without_subtitle(self):
        self.assertEqual(self.add_post().get_meta_description(), "Post")

    def test_long_subtitle_is_truncated(self):
        self.assertEqual(len(self.add_post(post_subtitle="x" * 300).get_meta_description()), 160)
