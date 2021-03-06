# Generated by Django 3.1 on 2021-03-19 14:35

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20210319_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.core.fields.StreamField([('html', wagtail.core.blocks.RawHTMLBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr'])), ('post_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an Image', label='Image', required=True)), ('caption', wagtail.core.blocks.CharBlock(help_text='Provide a caption for the image', label='Caption', required=True))]))], blank=True, null=True),
        ),
    ]
