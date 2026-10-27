from django.db import models
from django.conf import settings

class Review(models.Model):
    AI_PROVIDER_CHOICES = [
        ('rules', 'Rule-based'),
        ('gensara', 'GenSeraLabs'),
        ('custom', 'Custom OpenAI-compatible'),
        ('local', 'Ollama'),
    ]
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
    ai_review = models.TextField(blank=True, default='')
    ai_review_error = models.TextField(blank=True, default='')
    ai_provider = models.CharField(max_length=20, choices=AI_PROVIDER_CHOICES, default='rules')
    ai_model = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'project_name': self.project.name,
            'overall_score': self.overall_score,
            'compliance_score': self.compliance_score,
            'quality_score': self.quality_score,
            'status': self.status,
            'ai_provider': self.ai_provider,
            'created_at': self.created_at.isoformat(),
        }

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


class CodeReviewSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='code_reviews', null=True, blank=True)
    title = models.CharField(max_length=255, default='Code Review')
    input_type = models.CharField(max_length=50, default='paste')  # paste, file, zip
    files_reviewed = models.JSONField(default=list)
    provider = models.CharField(max_length=50, default='gensara')
    model = models.CharField(max_length=200, blank=True, default='')
    review_output = models.TextField()
    summary = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'input_type': self.input_type,
            'files': self.files_reviewed,
            'provider': self.provider,
            'model': self.model,
            'summary': self.summary,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }

    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=255, default='New conversation')
    provider = models.CharField(max_length=50, default='gensara')
    model = models.CharField(max_length=200, blank=True, default='')
    context_type = models.CharField(max_length=50, blank=True, default='')  # 'code_review', 'project', etc.
    context_ref_id = models.CharField(max_length=64, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'title': self.title,
            'provider': self.provider,
            'model': self.model,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'message_count': self.messages.count(),
        }

    def __str__(self):
        return f"{self.title} ({self.session_id})"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20)  # user, assistant, system
    content = models.TextField()
    provider = models.CharField(max_length=50, blank=True, default='')
    model = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'provider': self.provider,
            'model': self.model,
            'created_at': self.created_at.isoformat(),
        }

    def __str__(self):
        return f"{self.role}: {self.content[:40]}"
