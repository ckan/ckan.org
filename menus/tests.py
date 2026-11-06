from django.test import TestCase
from stories.models import StoriesPage
from wagtail.models import Page

from menus.models import Menu, MenuItem


class ShowcaseDropdownTests(TestCase):
    """The header "Showcase" item is a dropdown: Data Portals + Success Stories (#345)."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.stories = home.add_child(instance=StoriesPage(title="Success stories", slug="success-stories"))
        menu = Menu.objects.create(title="Header menu", slug="header-menu")
        for order, (title, url) in enumerate([("Features", "/features"), ("Showcase", "/showcase"), ("Solutions", "/solutions")]):
            MenuItem.objects.create(page=menu, link_title=title, link_url=url, sort_order=order)

    def test_showcase_renders_as_dropdown(self):
        response = self.client.get(self.stories.url)

        self.assertContains(response, 'id="dropbtn-Showcase" aria-expanded="false" aria-controls="Showcase_dropdown"')
        self.assertContains(response, '<a href="/showcase">Data Portals</a>', html=True)
        self.assertContains(response, '<a href="/success-stories">Success Stories</a>', html=True)
        # The plain "Showcase" link is replaced by the dropdown; other items are untouched.
        self.assertEqual(response.content.decode().count('href="/showcase"'), 1)
        self.assertContains(response, 'href="/features"')

    def test_data_portals_uses_the_menu_item_url(self):
        MenuItem.objects.filter(link_title="Showcase").update(link_url="/portals")

        response = self.client.get(self.stories.url)

        self.assertContains(response, '<a href="/portals">Data Portals</a>', html=True)

    def test_showcase_is_active_on_success_stories(self):
        response = self.client.get(self.stories.url)

        self.assertRegex(response.content.decode(), r'id="dropbtn-Showcase"[^>]*class="active"')
        self.assertNotRegex(response.content.decode(), r'id="dropbtn-Solutions"[^>]*class="active"')
