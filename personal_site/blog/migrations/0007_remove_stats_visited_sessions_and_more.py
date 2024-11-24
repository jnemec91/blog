# Generated by Django 5.0 on 2024-11-24 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_stats_visited_sessions_stats_voted_sessions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stats',
            name='visited_sessions',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='voted_sessions',
        ),
        migrations.AddField(
            model_name='stats',
            name='visited',
            field=models.JSONField(default={'sessions': []}, verbose_name='visited sessions'),
        ),
        migrations.AddField(
            model_name='stats',
            name='voted',
            field=models.JSONField(default={'sessions': []}, verbose_name='voted sessions'),
        ),
    ]
