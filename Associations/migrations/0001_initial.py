# Generated by Django 4.1.7 on 2023-03-30 16:34

import Associations.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Associations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('about', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('logo', models.ImageField(upload_to=Associations.models.logo_upload_handler)),
                ('banner', models.ImageField(upload_to=Associations.models.banner_upload_handler)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Associations',
            },
        ),
        migrations.CreateModel(
            name='AssociationsGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Associations.associations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Associations Group',
            },
        ),
        migrations.AddConstraint(
            model_name='associationsgroup',
            constraint=models.UniqueConstraint(fields=('association', 'user'), name='unique_user_association'),
        ),
    ]