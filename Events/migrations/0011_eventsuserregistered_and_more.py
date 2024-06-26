# Generated by Django 4.1.7 on 2023-04-14 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Events', '0010_eventsattendee_eventsattendee_unique_user_attendees'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsUserRegistered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Events User Attendee',
            },
        ),
        migrations.RemoveConstraint(
            model_name='eventsattendee',
            name='unique_user_attendees',
        ),
        migrations.RemoveField(
            model_name='eventsattendee',
            name='attended_time',
        ),
        migrations.RemoveField(
            model_name='eventsattendee',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventsattendee',
            name='is_attended',
        ),
        migrations.RemoveField(
            model_name='eventsattendee',
            name='user',
        ),
        migrations.AddField(
            model_name='eventsuserregistered',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Events.events'),
        ),
        migrations.AddField(
            model_name='eventsuserregistered',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventsattendee',
            name='user_registered',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='Events.eventsuserregistered'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='eventsuserregistered',
            constraint=models.UniqueConstraint(fields=('event', 'user'), name='unique_user_registered'),
        ),
    ]
