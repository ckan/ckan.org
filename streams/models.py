from django.db import models

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.fields import (
    StreamField,
)

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel
)

from wagtail.snippets.models import register_snippet


@register_snippet
class GeneralFeature(models.Model):

    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )  
    title = models.CharField(
        max_length=64,
        help_text='Title of the General Feature',
    )
    sub_title = models.CharField(
        max_length=512,
        help_text='Subtitle',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    text = models.TextField(
        max_length=2056,
        help_text='Add some text to the Feature',
    )
    read_more_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        help_text='Select an internal Page to link to',
        related_name='+',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('icon'),
                FieldPanel('title'),
                FieldPanel('sub_title'),
                FieldPanel('image'),
                FieldPanel('text'),
                FieldPanel('read_more_page'),
            ],
            heading = "General Feature"
        )
    ]

    class Meta:
        verbose_name = "General Feature"
        verbose_name_plural = "General Features"


@register_snippet
class Feature(models.Model):

    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )  
    title = models.CharField(
        max_length=64,
        help_text='Title of the Feature',
    )
    sub_title = models.CharField(
        max_length=512,
        help_text='Subtitle',
    )
    read_more_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        help_text='Select an internal Page to link to',
        related_name='+',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('icon'),
                FieldPanel('title'),
                FieldPanel('sub_title'),
                FieldPanel('read_more_page'),
            ],
            heading = "Feature"
        )
    ]

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"


@register_snippet
class Extension(models.Model):

    title = models.CharField(
        max_length=64,
        help_text='Title of the Extension',
    )
    author = models.CharField(
        max_length=128,
        help_text='Subtitle',
    )
    description = models.CharField(
        max_length=512,
        help_text='Subtitle',
    )
    rating = models.CharField(
        max_length=32,
        help_text='Add repository rating in this format: "4.51 (240)"',
    )
    url = models.URLField(
        help_text='Add this Extension URL'
    )

    def __str__(self):
        return self.title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('author'),
                FieldPanel('description'),
                FieldPanel('rating'),
                FieldPanel('url'),
            ],
            heading = "Extension"
        )
    ]

    class Meta:
        verbose_name = "Extension"
        verbose_name_plural = "Extensions"



@register_snippet
class SoftwareEngineer(models.Model):

    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )  
    name = models.CharField(
        max_length=128,
    )
    role = models.CharField(
        max_length=256,
    )
    twitter = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )
    linkedin = models.CharField(
        null=True,
        blank=True,        
        max_length=512,
    )
    github = models.CharField(
        null=True,
        blank=True,        
        max_length=512,
    )
    active = models.BooleanField(
        default=True,
        help_text='Uncheck this field for former tech team member',
    )

    def __str__(self):
        return self.name

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('photo'),
                FieldPanel('name'),
                FieldPanel('role'),
                FieldPanel('twitter'),
                FieldPanel('linkedin'),
                FieldPanel('github'),
                FieldPanel('active'),
            ],
            heading = "Software Engineer"
        )
    ]

    class Meta:
        verbose_name = "Software Engineer"
        verbose_name_plural = "Software Engineers"



@register_snippet
class Steward(models.Model):

    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )  
    name = models.CharField(
        max_length=128,
    )
    about = models.TextField(
        max_length=1028,
    )
    represented_by = models.CharField(
        null=True,
        blank=True,
        max_length=256,
    )
    link = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )
    twitter = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )
    linkedin = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )
    skype = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )    
    github = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )

    def __str__(self):
        return self.name

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('photo'),
                FieldPanel('name'),
                FieldPanel('about'),
                FieldPanel('represented_by'),
                FieldPanel('link'),
                FieldPanel('twitter'),
                FieldPanel('linkedin'),
                FieldPanel('skype'),
                FieldPanel('github'),
            ],
            heading = "Steward"
        )
    ]

    class Meta:
        verbose_name = "Steward"
        verbose_name_plural = "Stewards"


@register_snippet
class CkanForCard(models.Model):

    title = models.CharField(
        max_length=64,
        help_text='Title of the card',
        default='Card title',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    text = models.TextField(
        max_length=1024,
        help_text='Add some text to the card',
        default = 'Card text',
    )
    link_text = models.CharField(
        max_length=64,
        help_text='Add some text for the link',
        default='Link text',
    )
    internal_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        help_text='Select an internal Page to link to',
        related_name='+',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('image'),
                FieldPanel('text'),
                FieldPanel('link_text'),
                FieldPanel('internal_page'),
            ],
            heading = "Ckan For ... Card"
        )
    ]

    class Meta:
        verbose_name = "Ckan for ... Card"
        verbose_name_plural = "Ckan for ... Cards"


@register_snippet
class PoweredCard(models.Model):
    title = models.CharField(
        max_length=64,
        help_text='Title of the card',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    text = models.TextField(
        max_length=1024,
        help_text='Add some text to the card',
    )
    link = models.URLField(
        help_text='Add a URL to the source site'
    )

    def __str__(self):
        return self.title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('image'),
                FieldPanel('text'),
                FieldPanel('link'),
            ],
            heading = "Powered by CKAN Card"
        )
    ]

    class Meta:
        verbose_name = "Powered by CKAN Card"
        verbose_name_plural = "Powered by CKAN Cards"


class GitCardBlock(blocks.StructBlock):

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image_top', ImageChooserBlock(required=True)),
                ('text', blocks.TextBlock(required=True, max_length=2048)),
                ('image_bottom', ImageChooserBlock(required=True)),
                ('external_link', blocks.URLBlock()),
            ]
        )
    )

    class Meta:
        template = 'snippets/git_card_block.html',
        icon = "placeholder",
        label = "CKAN Git Card"


class PoweringOpendataBlock(blocks.StructBlock):

    images = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=True)),
                ('external_link', blocks.URLBlock()),
            ]
        )
    )

    class Meta:
        icon = "image",
        label = "Powering Opendata Images"



@register_snippet
class WorkingGroup(models.Model):

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )  
    name = models.CharField(
        max_length=64,
        help_text='Name of this working group',
    )
    description = models.TextField(
        max_length=1024,
        help_text='Describe this working group',
    )
    member_1_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    member_1_description = models.TextField(
        max_length=1024,
        help_text='Describe this member',
    )
    member_1_url = models.URLField(
        max_length=256,
        help_text='Provide this member URL',
    )
    member_2_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    member_2_description = models.TextField(
        max_length=1024,
        help_text='Describe this member',
    )
    member_2_url = models.URLField(
        max_length=256,
        help_text='Provide this member URL',
    )
    member_3_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    member_3_description = models.TextField(
        max_length=1024,
        help_text='Describe this member',
    )
    member_3_url = models.URLField(
        max_length=256,
        help_text='Provide this member URL',
    )
    additional_text = models.TextField(
        max_length=2056,
        help_text='Describe this working group',
    )    
    email = models.EmailField(
        null=True,
        blank=True,
        help_text='Provide e-mail to contact Working Group'
    )

    def __str__(self):
        return self.name

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('image'),
                FieldPanel('name'),
                FieldPanel('description'),
                MultiFieldPanel(
                    [
                        FieldPanel('member_1_image'),
                        FieldPanel('member_1_description'),
                        FieldPanel('member_1_url'),
                    ],
                    heading = "Member 1"
                ),
                MultiFieldPanel(
                    [
                        FieldPanel('member_2_image'),
                        FieldPanel('member_2_description'),
                        FieldPanel('member_2_url'),
                    ],
                    heading = "Member 2"
                ),
                MultiFieldPanel(
                    [
                        FieldPanel('member_3_image'),
                        FieldPanel('member_3_description'),
                        FieldPanel('member_3_url'),
                    ],
                    heading = "Member 3"
                ),                
                FieldPanel('additional_text'),
                FieldPanel('email'),
            ],
            heading = "Working Group"
        )
    ]

    class Meta:
        verbose_name = "Working Group"
        verbose_name_plural = "Working Groups"


@register_snippet
class Feedback(models.Model):

    name = models.CharField(
        max_length=64,
        help_text='Name of the person',
    )
    role = models.CharField(
        max_length=64,
        help_text='Who is the the person?',
    )    
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    text = models.TextField(
        max_length='2056',
        help_text='What was told',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('role'),
                FieldPanel('image'),
                FieldPanel('text'),
            ],
            heading = "Feedbacks"
        )
    ]


    def __str__(self):
        return f'{self.name}: {self.text}'


@register_snippet
class PoweringImage(models.Model):

    title = models.CharField(
        max_length=64,
        help_text='Title of the block',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    link = models.URLField(
        help_text='Add a URL to the block'
    )

    def __str__(self):
        return self.title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('image'),
                FieldPanel('link'),
            ],
            heading = "Powering open data item"
        )
    ]


@register_snippet
class Commercial(models.Model):

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    name = models.CharField(
        max_length=128,
    )
    url = models.URLField(
        help_text='Add this Company URL'
    )
    level = models.CharField(
        max_length=256,
    )
    about = models.TextField(
        max_length=1028,
    )
    date_info =  models.TextField(
        max_length=128,
    )

    def __str__(self):
        return self.name

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('image'),
                FieldPanel('name'),
                FieldPanel('url'),
                FieldPanel('level'),
                FieldPanel('about'),
                FieldPanel('date_info')
            ],
            heading = "Commercial"
        )
    ]

    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commercials"
