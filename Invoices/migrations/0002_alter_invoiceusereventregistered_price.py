# Generated by Django 4.1.7 on 2023-05-01 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceusereventregistered',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
