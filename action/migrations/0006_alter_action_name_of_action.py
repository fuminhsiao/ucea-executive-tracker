# Generated by Django 5.0.6 on 2025-03-12 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0005_alter_action_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='name_of_action',
            field=models.CharField(max_length=500),
        ),
    ]
