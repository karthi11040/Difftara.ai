from rest_framework import serializers
from accounts.models import User
from projects.models import Project
from requirements_app.models import Requirement
from reviews.models import Review, Finding, MentorReview
from activities.models import Activity
from projects.utils import validate_zip_upload, validate_srs_upload

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['id', 'requirement_id', 'description', 'category', 'priority', 'active']

class MentorReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.ReadOnlyField(source='reviewer.username')
    class Meta:
        model = MentorReview
        fields = ['id', 'reviewer', 'reviewer_name', 'original_status', 'final_status', 'comment', 'is_correct', 'reviewed_at']

class FindingSerializer(serializers.ModelSerializer):
    current_status = serializers.ReadOnlyField()
    req_code = serializers.SerializerMethodField()
    mentor_override = MentorReviewSerializer(read_only=True)

    class Meta:
        model = Finding
        fields = ['id', 'requirement', 'req_code', 'status', 'current_status', 'evidence_file', 'evidence_function', 'description', 'suggestion', 'priority', 'mentor_override']

    def get_req_code(self, obj):
        return obj.requirement.requirement_id if obj.requirement else 'QUALITY'

class ReviewSerializer(serializers.ModelSerializer):
    findings = FindingSerializer(many=True, read_only=True)
    mentor_name = serializers.ReadOnlyField(source='mentor.username')

    class Meta:
        model = Review
        fields = ['id', 'project', 'mentor', 'mentor_name', 'status', 'overall_score', 'compliance_score', 'quality_score', 'testing_score', 'doc_score', 'created_at', 'findings']

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    requirements = RequirementSerializer(many=True, read_only=True)
    latest_score = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'owner_name', 'zip_file', 'srs_file', 'status', 'created_at', 'requirements', 'latest_score']
        read_only_fields = ['owner', 'owner_name', 'status', 'created_at', 'requirements', 'latest_score']

    def validate_zip_file(self, value):
        validate_zip_upload(value)
        return value

    def validate_srs_file(self, value):
        if value:
            validate_srs_upload(value)
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('srs_file'):
            raise serializers.ValidationError({'srs_file': 'An SRS document is required when creating projects through the API.'})
        return attrs

    def get_latest_score(self, obj):
        latest = obj.reviews.filter(status='completed').order_by('-created_at').first()
        return latest.overall_score if latest else None

class ActivitySerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Activity
        fields = ['id', 'user', 'username', 'project', 'project_name', 'action', 'message', 'created_at']
