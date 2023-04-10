from django.contrib import admin

from .models import UserNotification, UserNotificationAction

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'is_read', 'sender', 'created_at', 'updated_at')


@admin.register(UserNotificationAction)
class UserNotificationActionAdmin(admin.ModelAdmin):
    list_display = ('notification', 'target_id', 'type', 'label', 'style', 'is_priority', 'created_at')
