from django.db import models

class Requirement(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='requirements')
    requirement_id = models.CharField(max_length=50) # e.g. REQ-001
    description = models.TextField()
    category = models.CharField(max_length=100, default='General')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='High')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['requirement_id']

    def __str__(self):
        return f"{self.requirement_id}: {self.description[:50]}"
