from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0017_populate_uuid_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="pipelineartifact",
            name="artifact_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.artifact",
                to_field="uuid",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="pipeline",
            name="definition_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinition",
                to_field="uuid",
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="definition_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinitiontaskdefinition",
                to_field="uuid",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="pipelinedefinitiontaskdefinition",
            name="pipeline_definition_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinition",
                to_field="uuid",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]
