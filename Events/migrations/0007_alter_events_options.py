# Generated by Django 4.1.7 on 2023-04-02 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0006_events_association'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='events',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Events'},
        ),
    ]
