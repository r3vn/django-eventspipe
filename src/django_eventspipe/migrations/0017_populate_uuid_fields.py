import uuid
from django.db import migrations, models


def populate_uuids(apps, schema_editor):
    model_names = [
        "Artifact",
        "PipelineArtifact",
        "PipelineDefinition",
        "PipelineDefinitionTaskDefinition",
    ]

    for model_name in model_names:
        Model = apps.get_model("django_eventspipe", model_name)

        for obj in Model.objects.filter(uuid__isnull=True).only("pk").iterator():
            Model.objects.filter(pk=obj.pk).update(uuid=uuid.uuid4())


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0016_add_uuid_fields"),
    ]

    operations = [
        migrations.RunPython(
            populate_uuids,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="artifact",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                unique=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="pipelineartifact",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                unique=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="pipelinedefinition",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                unique=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                unique=True,
                editable=False,
            ),
        ),
    ]
