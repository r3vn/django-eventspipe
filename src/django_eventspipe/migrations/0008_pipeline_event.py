# Generated by Django 5.1.2 on 2024-10-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_eventspipe', '0007_rename_filters_pipelinedefinition_rules_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='event',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]