# Generated by Django 4.1.7 on 2023-03-31 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Associations', '0002_associationsgroup_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='associations',
            name='is_disabled',
            field=models.BooleanField(default=False),
        ),
    ]
