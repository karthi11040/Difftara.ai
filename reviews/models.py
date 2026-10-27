from django.db import models
from django.conf import settings

class Review(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='reviews')
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_reviews')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    overall_score = models.IntegerField(default=0)
    compliance_score = models.FloatField(default=0.0)
    quality_score = models.FloatField(default=0.0)
    testing_score = models.FloatField(default=0.0)
    doc_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review #{self.id} for {self.project.name} - Score: {self.overall_score}%"

class Finding(models.Model):
    STATUS_CHOICES = [
        ('Implemented', 'Implemented'),
        ('Partial', 'Partial'),
        ('Missing', 'Missing'),
        ('Manual Review', 'Manual Review'),
    ]
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='findings')
    requirement = models.ForeignKey('requirements_app.Requirement', on_delete=models.SET_NULL, null=True, blank=True, related_name='findings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Missing')
    evidence_file = models.CharField(max_length=255, blank=True, default='')
    evidence_function = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    suggestion = models.TextField(blank=True, default='')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='High')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def current_status(self):
        if hasattr(self, 'mentor_override') and self.mentor_override:
            return self.mentor_override.final_status
        return self.status

    def __str__(self):
        return f"Finding ({self.current_status}): {self.description[:50]}"

class MentorReview(models.Model):
    finding = models.OneToOneField(Finding, on_delete=models.CASCADE, related_name='mentor_override')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_status = models.CharField(max_length=20)
    final_status = models.CharField(max_length=20)
    comment = models.TextField(blank=True, default='')
    is_correct = models.BooleanField(default=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Override by {self.reviewer.username} on Finding #{self.finding.id}"
