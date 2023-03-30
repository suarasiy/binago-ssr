from django.contrib import admin
from .models import Events, EventsCategories, EventsExtendedUrl


class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'price', 'is_published', 'updated_at')
    prepopulated_fields = {
        'slug': ('title',)
    }


class EventsCategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {
        'slug': ('category',)
    }


admin.site.register(Events, EventsAdmin)
admin.site.register(EventsCategories, EventsCategoriesAdmin)
