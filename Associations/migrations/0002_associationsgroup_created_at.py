# Generated by Django 4.1.7 on 2023-03-30 17:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Associations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='associationsgroup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]