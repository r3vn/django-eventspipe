from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0019_populate_uuid_foreign_keys"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pipelineartifact",
            name="artifact_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.artifact",
                to_field="uuid",
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="pipeline_definition_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinition",
                to_field="uuid",
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]
