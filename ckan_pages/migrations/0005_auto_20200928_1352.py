# Generated by Django 3.1.1 on 2020-09-28 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ckan_pages', '0004_ckanforpage_feedbackitems_pwereditems_workinggroupitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ckanforpage',
            name='page_for',
            field=models.CharField(blank=True, help_text='CKAN for: government / enterprise', max_length=512),
        ),
    ]
