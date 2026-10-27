from django.db import models
from django.conf import settings

class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    action = models.CharField(max_length=100) # e.g. "PROJECT_UPLOAD", "REVIEW_RUN", "MENTOR_OVERRIDE"
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.action}] {self.user.username}: {self.message[:50]}"

class ActivityService:
    @staticmethod
    def record(user, action, message, project=None):
        return Activity.objects.create(
            user=user,
            project=project,
            action=action,
            message=message
        )
