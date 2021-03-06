# Generated by Django 3.1.1 on 2020-09-25 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0052_pagelogentry'),
        ('blog', '0007_auto_20200925_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogListingPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('page_subtitle', models.CharField(blank=True, help_text='Page subtitle. Goes under the header.', max_length=128, null=True)),
                ('page_caption', models.CharField(blank=True, help_text='Page caption. Goes under the page subtitle.', max_length=512, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
