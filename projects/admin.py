from django.contrib import admin
from accounts.admin import RoleBasedAdminMixin
from projects.models import Project


@admin.register(Project)
class ProjectAdmin(RoleBasedAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'owner', 'assigned_mentor', 'status', 'is_archived', 'created_at')
    list_filter = ('status', 'is_archived', 'created_at')
    search_fields = ('name', 'owner__username', 'assigned_mentor__username')
