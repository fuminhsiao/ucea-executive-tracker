# Generated by Django 5.0.6 on 2025-03-17 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0008_alter_action_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='news_commentary',
        ),
        migrations.AddField(
            model_name='action',
            name='news_link',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='news_title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
