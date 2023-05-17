# Generated by Django 4.1.7 on 2023-05-16 03:00

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    models = {
        'invoice_event_post': apps.get_model("Invoices", "invoiceeventpost"),
        'invoice_user_event_registered': apps.get_model("Invoices", "invoiceusereventregistered")
    }
    for row in models["invoice_event_post"].objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])
    for row in models['invoice_user_event_registered'].objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])


class Migration(migrations.Migration):

    dependencies = [
        ('Invoices', '0008_invoiceeventpost_midtrans_token_and_more'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
