# Generated by Django 4.1.7 on 2023-05-03 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0014_rename_url_title_eventsextendedurl_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsextendedurl',
            name='is_attended',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
