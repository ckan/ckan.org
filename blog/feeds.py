from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.utils.feedgenerator import Atom1Feed

from .models import BlogPostPage


class RssBlogPostPageFeeds(Feed):
    title = "CKAN Blog posts"
    link = "https://ckan.org/blog"
    description = "Recent news, industry reports and announcements"

    def items(self):
        return BlogPostPage.objects.order_by("-created")[:100]

    def item_title(self, item):
        return item.post_title

    def item_link(self, item):
        return item.full_url

    def item_description(self, item):
        return truncatewords(item.post_subtitle, 30)

    def item_pubdate(self, item):
        return item.created

    def item_author_name(self, item):
        return item.author


class AtomBlogPostPageFeeds(RssBlogPostPageFeeds):
    feed_type = Atom1Feed
    subtitle = RssBlogPostPageFeeds.description