from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageWithCaption(blocks.StructBlock):

    image = ImageChooserBlock(
        label="Image",
        required=True,
        help_text="Add an image expanded to fill the entire screen width"
    )
    caption = blocks.CharBlock(
        label="Caption",
        required=False,
        help_text="Provide a caption for the image"
    )

    class Meta:
        template = "blog/blocks/imagewithcaption.html"
        form_classname = "imagewithcaption"
        icon = "image"
