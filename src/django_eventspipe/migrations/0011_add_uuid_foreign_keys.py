from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0010_populate_uuid_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="pipeline_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipeline",
                to_field="uuid",
                db_column="pipeline_uuid_id",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
            ),
        ),

        migrations.AddField(
            model_name="pipelineartifact",
            name="pipeline_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipeline",
                to_field="uuid",
                db_column="pipeline_uuid_id",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
            ),
        ),
    ]
