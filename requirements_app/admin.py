from django.contrib import admin
from accounts.admin import RoleBasedAdminMixin
from requirements_app.models import Requirement


@admin.register(Requirement)
class RequirementAdmin(RoleBasedAdminMixin, admin.ModelAdmin):
    list_display = ('requirement_id', 'project', 'category', 'priority', 'active')
    list_filter = ('category', 'priority', 'active')
    search_fields = ('requirement_id', 'description', 'project__name')
