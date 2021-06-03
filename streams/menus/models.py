from django.db import models

from django_extensions.db.fields import AutoSlugField

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.core.models import Orderable

class Menu(ClusterableModel):

    title = models.CharField(max_length=64)
    slug = AutoSlugField(
        populate_from = 'title',
        editable = True,
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel('menu_items', label='Menu Item'),
    ]

    def __str__(self):
        return self.title


class MenuItem(Orderable):
    link_title = models.CharField(
        max_length=64,
    )
    link_url = models.CharField(
        max_length=256,
        blank=True,
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE
    )
    open_in_new_tab = models.BooleanField(
        null=True,
        default=False
    )
    show_as_button = models.BooleanField(
        null=True,
        default=False
    )
    svg_icon = models.TextField(
        max_length='2048',
        null=True,
        blank=True,
    )
    icon_before_text = models.BooleanField(
        null=True,
        default=False
    )

    panels = [
        FieldPanel('link_title'),
        FieldPanel('link_url'),
        PageChooserPanel('link_page'),
        FieldPanel('open_in_new_tab'),
        FieldPanel('show_as_button'),
        FieldPanel('svg_icon'),
        FieldPanel('icon_before_text'),
    ]

    page = ParentalKey(Menu, related_name = 'menu_items')

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'
