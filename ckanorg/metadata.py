from django.utils.text import Truncator

# Fields that hold a page's one-line summary, in order of preference.
SUMMARY_FIELDS = ("post_subtitle", "subtitle", "page_subtitle")


class MetaDescriptionFallbackMixin:
    """Fall back to the page's subtitle when the editor left the Promote tab's
    search description empty, so every page gets exactly one non-empty
    <meta name="description"> from wagtail-metadata."""

    def get_meta_description(self):
        if self.search_description:
            return self.search_description
        for field in SUMMARY_FIELDS:
            value = getattr(self, field, None)
            if value:
                return Truncator(value).chars(160)
        return self.title
