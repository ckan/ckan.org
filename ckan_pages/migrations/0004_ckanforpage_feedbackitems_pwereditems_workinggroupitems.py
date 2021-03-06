# Generated by Django 3.1.1 on 2020-09-28 13:44

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0052_pagelogentry'),
        ('wagtailimages', '0022_uploadedimage'),
        ('streams', '0002_auto_20200928_0605'),
        ('ckan_pages', '0003_auto_20200928_0605'),
    ]

    operations = [
        migrations.CreateModel(
            name='CkanForPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('page_for', wagtail.core.fields.StreamField([('working_group', wagtail.core.blocks.ChoiceBlock(choices=[('government', 'CKAN for Government'), ('enterprise', 'CKAN for Enterprise')], help_text='Select CKAN for Government/Enterprise'))])),
                ('subtitle', models.CharField(blank=True, help_text='Subtitle text under the header', max_length=512)),
                ('upper_text', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr']))])),
                ('bottom_text', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr']))], blank=True, null=True)),
                ('image', models.ForeignKey(help_text='Main image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='WorkingGroupItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('group_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streams.workinggroup')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_items', to='ckan_pages.ckanforpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PweredItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='powered_items', to='ckan_pages.ckanforpage')),
                ('powered_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streams.poweredcard')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeedbackItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('feedback_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streams.feedback')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_items', to='ckan_pages.ckanforpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
