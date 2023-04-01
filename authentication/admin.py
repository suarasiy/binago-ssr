from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User


class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'is_verified', 'is_staff', 'is_active', 'updated_at')
    readonly_fields = ['avatar_preview']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "gender")}),
        (_("Extra"), {"fields": ("avatar", "banner", "avatar_preview")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_active",
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


admin.site.register(User, UserAdmin)
