import io

from django.core.files.images import ImageFile
from django.test import TestCase
from PIL import Image as PILImage
from wagtail.images.models import Image
from wagtail.models import Page

from ckan_pages.models import CommunityPage


def make_image():
    buffer = io.BytesIO()
    PILImage.new("RGB", (20, 20)).save(buffer, "PNG")
    image = Image(title="test")
    image.file.save("test.png", ImageFile(buffer, name="test.png"), save=False)
    image.save()
    return image


class CommunityHelpBlockTests(TestCase):
    """The get-involved / need-help section of the community page (#348)."""

    @classmethod
    def setUpTestData(cls):
        image = make_image()
        images = {
            field.name: image
            for field in CommunityPage._meta.get_fields()
            if field.concrete and getattr(field, "related_model", None) is Image
        }
        home = Page.objects.get(slug="home")
        cls.page = home.add_child(instance=CommunityPage(title="Community", slug="community", subtitle="Community", **images))

    def setUp(self):
        self.response = self.client.get(self.page.url)

    def test_links_to_the_community_forum(self):
        self.assertContains(self.response, 'href="https://discuss.okfn.org/c/ckan/35"', count=2)

    def test_docs_link_points_to_the_documentation(self):
        # It used to point at "/", the ckan.org home page.
        self.assertContains(self.response, '<a href="https://docs.ckan.org/en/" target="_blank" rel="noopener">CKAN docs</a>', html=True)

    def test_rockstar_tickets_use_the_current_github_projects_url(self):
        self.assertContains(self.response, "https://github.com/orgs/ckan/projects/9")
        self.assertNotContains(self.response, "github.com/ckan/ckan/projects/4")

    def test_styles_live_in_main_css_not_inline(self):
        self.assertContains(self.response, 'class="container community-help"')
        self.assertNotContains(self.response, ".grey-card p a")
