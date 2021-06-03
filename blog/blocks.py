from django.db import models
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageWithCaption(blocks.StructBlock):

    image = ImageChooserBlock(label="Image", required=True, help_text="Add an Image")
    caption = blocks.CharBlock(label="Caption", required=True, help_text="Provide a caption for the image")

    class Meta:
        template = 'blog/blocks/imagewithcaption.html'
        form_classname = 'imagewithcaption'
        icon = 'picture'
