# Generated by Django 4.1.7 on 2023-03-27 16:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='url_custom',
            new_name='url_homepage',
        ),
        migrations.RenameField(
            model_name='events',
            old_name='url',
            new_name='url_stream',
        ),
        migrations.RemoveField(
            model_name='events',
            name='url_youtube',
        ),
        migrations.RemoveField(
            model_name='eventscategories',
            name='created_by',
        ),
        migrations.AddField(
            model_name='events',
            name='price',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='events',
            name='schedule_end',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='events',
            name='schedule_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]