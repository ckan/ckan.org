import io
import re

from django.core.files.images import ImageFile
from django.test import TestCase
from PIL import Image as PILImage
from wagtail.images.models import Image
from wagtail.models import Page

from blog.models import BlogListingPage, BlogPostPage


def make_image(width, height):
    buffer = io.BytesIO()
    PILImage.new("RGB", (width, height), "white").save(buffer, "PNG")
    image = Image(title="featured")
    image.file.save("featured.png", ImageFile(buffer, name="featured.png"), save=False)
    image.save()
    return image


class FeaturedImageSrcsetTests(TestCase):
    """Featured images get a 2x rendition for high-DPI screens (#366)."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.blog = home.add_child(instance=BlogListingPage(title="Blog", slug="blog"))

    def add_post(self, **kwargs):
        return self.blog.add_child(instance=BlogPostPage(title="Post", post_title="Post", slug="post", **kwargs))

    def featured_img(self, post):
        response = self.client.get(post.url)
        self.assertEqual(response.status_code, 200)
        match = re.search(r'<img [^>]*srcset="[^"]*fill-1440x600[^>]*>', response.content.decode())
        return match and match.group(0)

    def test_large_original_gets_1x_and_2x_candidates(self):
        tag = self.featured_img(self.add_post(main_image=make_image(3000, 1250)))

        self.assertRegex(tag, r'src="[^"]*\.fill-1440x600\.png"')  # unchanged 1x URL
        self.assertRegex(tag, r'srcset="[^"]*\.fill-1440x600\.png 1440w, [^"]*\.fill-2880x1200\.png 2880w"')
        self.assertIn('sizes="(min-width: 1440px) 1440px, 100vw"', tag)
        self.assertIn('width="1440"', tag)
        self.assertIn('height="600"', tag)

    def test_smaller_original_is_never_upscaled(self):
        tag = self.featured_img(self.add_post(main_image=make_image(2400, 1000)))

        self.assertRegex(tag, r'\.fill-2880x1200\.png 2400w"')

    def test_post_without_featured_image_still_renders(self):
        response = self.client.get(self.add_post().url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("fill-1440x600", response.content.decode())
