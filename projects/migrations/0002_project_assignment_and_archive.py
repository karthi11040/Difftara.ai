import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def assign_previous_reviewer(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Review = apps.get_model('reviews', 'Review')
    for project in Project.objects.filter(assigned_mentor__isnull=True).iterator():
        previous = Review.objects.filter(project_id=project.pk, mentor__isnull=False).order_by('-created_at').first()
        if previous:
            Project.objects.filter(pk=project.pk).update(assigned_mentor_id=previous.mentor_id)


class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0001_initial'),
        ('reviews', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='assigned_mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(assign_previous_reviewer, migrations.RunPython.noop),
    ]
