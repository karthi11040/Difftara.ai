from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('reviews', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='review',
            name='ai_review',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='review',
            name='ai_review_error',
            field=models.TextField(blank=True, default=''),
        ),
    ]
