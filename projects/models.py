from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    zip_file = models.FileField(upload_to='zips/')
    srs_file = models.FileField(upload_to='srs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    extracted_path = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
