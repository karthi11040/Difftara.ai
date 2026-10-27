from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('reviews', '0002_review_ai_feedback')]

    operations = [
        migrations.AddField(
            model_name='review',
            name='ai_provider',
            field=models.CharField(choices=[('rules', 'Rule-based'), ('gensara', 'GenSeraLabs'), ('custom', 'Custom OpenAI-compatible'), ('local', 'Ollama')], default='rules', max_length=20),
        ),
        migrations.AddField(
            model_name='review',
            name='ai_model',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
