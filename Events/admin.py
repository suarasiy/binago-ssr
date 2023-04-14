from django.contrib import admin
from .models import Events, EventsCategories, EventsExtendedUrl, EventsUserRegistered, EventsAttendee


class EventsAdmin(admin.ModelAdmin):
    list_display = ('association_group', 'title', 'category', 'slug', 'price', 'is_published', 'updated_at')
    prepopulated_fields = {
        'slug': ('title',)
    }


class EventsCategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {
        'slug': ('category',)
    }


@admin.register(EventsUserRegistered)
class EventsUserRegisteredAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created_at', 'updated_at')


@admin.register(EventsAttendee)
class EventsAttendeeAdmin(admin.ModelAdmin):
    list_display = ('user_registered', 'created_at', 'updated_at')


admin.site.register(Events, EventsAdmin)
admin.site.register(EventsCategories, EventsCategoriesAdmin)
