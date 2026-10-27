from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from accounts.models import User
from projects.models import Project


def visible_projects(user):
    if user.is_admin_user:
        return Project.objects.all()
    if user.role == User.MENTOR:
        return Project.objects.filter(assigned_mentor=user)
    return Project.objects.filter(owner=user)


def can_manage_project(user, project):
    return user.is_admin_user or (user.role == User.MENTOR and project.assigned_mentor_id == user.pk)


def can_access_project(user, project):
    if user.is_admin_user:
        return True
    if user.role == User.MENTOR:
        return project.assigned_mentor_id == user.pk
    return project.owner_id == user.pk and not project.is_archived


def get_user_project(user, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not can_access_project(user, project):
        raise PermissionDenied
    return project
