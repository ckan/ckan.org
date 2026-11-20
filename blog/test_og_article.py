from django.test import TestCase
from wagtail.models import Page

from blog.models import BlogListingPage, BlogPostPage


class OpenGraphArticleTests(TestCase):
    """Blog posts declare og:type article with article:* dates (#383)."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.blog = home.add_child(instance=BlogListingPage(title="Blog", slug="blog"))
        self.post = self.blog.add_child(
            instance=BlogPostPage(title="Post", post_title="Post", slug="post", author="Jane Doe")
        )
        self.post.tags.add("security", "open data")
        self.post.save_revision().publish()

    def html(self, page):
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        return response.content.decode()

    def test_blog_post_is_an_article(self):
        html = self.html(self.post)
        self.assertEqual(html.count('property="og:type"'), 1)
        self.assertIn('<meta property="og:type" content="article">', html)
        self.assertRegex(html, r'<meta property="article:published_time" content="\d{4}-\d\d-\d\dT[^"]+">')
        self.assertRegex(html, r'<meta property="article:modified_time" content="\d{4}-\d\d-\d\dT[^"]+">')
        self.assertIn('<meta property="article:author" content="Jane Doe">', html)
        self.assertIn('<meta property="article:tag" content="security">', html)
        self.assertIn('<meta property="article:tag" content="open data">', html)

    def test_listing_page_is_not_an_article(self):
        self.assertNotIn('content="article"', self.html(self.blog))
