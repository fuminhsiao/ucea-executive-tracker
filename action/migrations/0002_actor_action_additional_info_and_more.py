# Generated by Django 5.0.6 on 2025-03-10 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='challenge_to_action',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='fallout',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='news_commentary',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='type_of_action',
            field=models.CharField(choices=[('Executive Order', 'Executive Order'), ('Agency action', 'Agency action'), ('Litigation', 'Litigation'), ('Agency Memo/Letter', 'Agency Memo/Letter'), ('Nomination/Appointment', 'Nomination/Appointment'), ('Congressional Action', 'Congressional Action'), ('Court Ruling/Action', 'Court Ruling/Action')], default='Agency action', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='actors',
            field=models.ManyToManyField(null=True, related_name='actions', to='action.actor'),
        ),
    ]
