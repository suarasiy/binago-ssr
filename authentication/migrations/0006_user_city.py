# Generated by Django 4.1.7 on 2023-04-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_user_about_user_institute_user_is_developer'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
