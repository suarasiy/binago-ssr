# Generated by Django 4.1.7 on 2023-03-31 13:44

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to=authentication.models.user_banner_upload_handler),
        ),
    ]