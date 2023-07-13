# Generated by Django 3.1.1 on 2020-09-21 07:55

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0052_pagelogentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('home_page_subtitle', models.CharField(blank=True, help_text='Subtitle text under the header', max_length=512)),
                ('ckan_git', wagtail.fields.StreamField([('cards', wagtail.blocks.StructBlock([('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image_top', wagtail.images.blocks.ImageChooserBlock(required=True)), ('text', wagtail.blocks.TextBlock(max_length=2048, required=True)), ('image_bottom', wagtail.images.blocks.ImageChooserBlock(required=True)), ('external_link', wagtail.blocks.URLBlock())])))]))], help_text='CKAN Git section', null=True)),
                ('powering_opendata_images', wagtail.fields.StreamField([('items', wagtail.blocks.StructBlock([('images', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('external_link', wagtail.blocks.URLBlock())])))]))], blank=True, help_text='Images for "Powering open data" section', null=True)),
                ('ckan_for_cards', wagtail.fields.StreamField([('cards', wagtail.blocks.StructBlock([('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(max_length=64, required=True)), ('text', wagtail.blocks.TextBlock(max_length=512, required=True)), ('link', wagtail.blocks.PageChooserBlock(help_text='Choose an internal page to link to', requuired=True)), ('link_text', wagtail.blocks.CharBlock(max_length=128, required=True))])))]))], blank=True, help_text='Cards for "CKAN for ..." section', null=True)),
                ('powered_by_ckan_cards', wagtail.fields.StreamField([('cards', wagtail.blocks.StructBlock([('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(max_length=64, required=True)), ('text', wagtail.blocks.TextBlock(max_length=512, required=True)), ('link', wagtail.blocks.URLBlock(help_text='Provide an external page to link to', requuired=True))])))]))], blank=True, help_text='Cards for "Powered by CKAN" section', null=True)),
                ('favicon', models.ForeignKey(blank=True, help_text='Favicon (16x16) for the site', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('home_page_subtitle_image', models.ForeignKey(help_text='The image that goes under the home page subtitle', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
