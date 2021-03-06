# Generated by Django 3.1.1 on 2020-09-25 06:38

import datetime
from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200925_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostpage',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('post_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an Image', label='Image', required=True)), ('caption', wagtail.core.blocks.CharBlock(help_text='Provide a caption for the image', label='Capture', required=True))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpostpage',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Post date'),
        ),
        migrations.AddField(
            model_name='blogpostpage',
            name='post_sub_title',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='blogpostpage',
            name='post_title',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
