# Generated by Django 4.1.7 on 2023-05-01 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoices', '0002_alter_invoiceusereventregistered_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceeventpost',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
