from django.contrib import admin
from .models import Associations, AssociationsGroup, AssociationsApprovalRequest


@admin.register(Associations)
class AssociationsAdmin(admin.ModelAdmin):
    list_display = ('approval', 'user', 'name', 'slug', 'email', 'is_active', 'created_at', 'updated_at')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(AssociationsGroup)
class AssociationsGroupAdmin(admin.ModelAdmin):
    list_display = ('association', 'user', 'is_approved', 'created_at', 'updated_at')


@admin.register(AssociationsApprovalRequest)
class AssociationsApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ('association', 'is_approved', 'created_at', 'updated_at')

    def association(self, obj):
        return obj.associations.name
