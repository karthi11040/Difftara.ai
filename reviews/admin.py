from django.contrib import admin
from accounts.admin import RoleBasedAdminMixin
from reviews.models import Finding, MentorReview, Review


@admin.register(Review)
class ReviewAdmin(RoleBasedAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'mentor', 'status', 'overall_score', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__name', 'mentor__username')


@admin.register(Finding)
class FindingAdmin(RoleBasedAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'review', 'requirement', 'status', 'priority')
    list_filter = ('status', 'priority')
    search_fields = ('description', 'evidence_file', 'requirement__requirement_id')


@admin.register(MentorReview)
class MentorReviewAdmin(RoleBasedAdminMixin, admin.ModelAdmin):
    list_display = ('finding', 'reviewer', 'is_correct', 'final_status', 'reviewed_at')
    list_filter = ('is_correct', 'final_status', 'reviewed_at')
    search_fields = ('finding__description', 'reviewer__username', 'comment')
