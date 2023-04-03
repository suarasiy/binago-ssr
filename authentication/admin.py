from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User


from django.utils.safestring import mark_safe


class UserAdmin(DefaultUserAdmin):
    list_display = ('icon', 'username', 'first_name', 'last_name', 'email',
                    'is_verified', 'is_staff', 'is_active', 'is_developer', 'updated_at')
    readonly_fields = ['avatar_preview']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "gender", "about")}),
        (_("Extra"), {"fields": ("avatar", "banner", "avatar_preview")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_developer",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_developer', 'created_at', 'updated_at',)

    def icon(self, obj):
        return mark_safe(f'<img src="{obj.avatar.url}" width="60" height="60" style="object-fit: cover; object-position: center; border-radius: 15px; margin-right: 5px;" />')


admin.site.register(User, UserAdmin)
