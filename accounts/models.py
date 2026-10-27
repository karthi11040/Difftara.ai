from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    MENTOR = 'mentor'
    STUDENT = 'student'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MENTOR, 'Mentor'),
        (STUDENT, 'Student'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    @property
    def is_admin_user(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_mentor_user(self):
        return self.role in [self.ADMIN, self.MENTOR] or self.is_superuser

    @property
    def is_student_user(self):
        return self.role == self.STUDENT

    def get_role_display(self):
        return 'Admin' if self.is_superuser else dict(self.ROLE_CHOICES).get(self.role, self.role)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if self.role == self.ADMIN:
            self.is_staff = True
        elif not self.is_superuser:
            self.is_staff = False
        super().save(*args, **kwargs)
