# Generated by Django 4.1.7 on 2023-05-03 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0015_alter_eventsextendedurl_is_attended'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='url_name',
            field=models.CharField(default='YouTube', max_length=50),
            preserve_default=False,
        ),
    ]
