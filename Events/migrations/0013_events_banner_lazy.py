# Generated by Django 4.1.7 on 2023-04-15 01:47

import Events.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0012_alter_eventsuserregistered_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='banner_lazy',
            field=models.ImageField(blank=True, default=None, max_length=500, null=True, upload_to=Events.models.banner_lazy_events_upload_handler),
        ),
    ]
