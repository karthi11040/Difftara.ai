from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from accounts.models import User


class RoleBasedAdminMixin:
    def has_module_permission(self, request):
        return request.user.is_admin_user or super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        return request.user.is_admin_user or super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_admin_user or super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin_user or super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin_user or super().has_delete_permission(request, obj)


@admin.register(User)
class UserAdmin(RoleBasedAdminMixin, DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (('Project role', {'fields': ('role',)}),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (('Project role', {'fields': ('role',)}),)
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = DjangoUserAdmin.list_filter + ('role',)
