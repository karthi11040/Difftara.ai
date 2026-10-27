from django.contrib import admin
from accounts.admin import RoleBasedAdminMixin
from activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(RoleBasedAdminMixin, admin.ModelAdmin):
    list_display = ('action', 'user', 'project', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('message', 'user__username', 'project__name')
    readonly_fields = ('user', 'project', 'action', 'message', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
