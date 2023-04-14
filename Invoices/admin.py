from django.contrib import admin

from .models import InvoiceEventPost, InvoiceUserEventRegistered


@admin.register(InvoiceEventPost)
class InvoiceEventPostAdmin(admin.ModelAdmin):
    list_display = ('event', 'price', 'discount', 'status', 'created_at', 'updated_at')


@admin.register(InvoiceUserEventRegistered)
class InvoiceUserEventRegisteredAdmin(admin.ModelAdmin):
    list_display = ('event_registered', 'price', 'discount', 'status', 'created_at', 'updated_at')
