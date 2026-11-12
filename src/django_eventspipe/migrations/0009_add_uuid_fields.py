import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0008_pipeline_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="pipeline",
            name="uuid",
            field=models.UUIDField(
                null=True,
                editable=False,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="uuid",
            field=models.UUIDField(
                null=True,
                editable=False,
            ),
        ),
    ]
