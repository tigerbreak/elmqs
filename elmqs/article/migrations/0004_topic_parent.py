# Generated by Django 4.2.16 on 2024-10-15 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_topic_articlepost_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='article.topic'),
        ),
    ]
