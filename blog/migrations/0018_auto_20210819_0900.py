# Generated by Django 3.1.13 on 2021-08-19 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20210818_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='author',
            field=models.CharField(blank=True, help_text='If value is empty, it will be filled by the current User.', max_length=255, null=True),
        ),
    ]
