from django.db import migrations


def populate_uuid_foreign_keys(apps, schema_editor):
    PipelineArtifact = apps.get_model(
        "django_eventspipe", "PipelineArtifact"
    )
    Pipeline = apps.get_model(
        "django_eventspipe", "Pipeline"
    )
    Task = apps.get_model(
        "django_eventspipe", "Task"
    )
    PipelineDefinitionTaskDefinition = apps.get_model(
        "django_eventspipe", "PipelineDefinitionTaskDefinition"
    )

    for obj in PipelineArtifact.objects.only(
        "pk", "artifact_id"
    ).iterator():
        if obj.artifact_id is not None:
            PipelineArtifact.objects.filter(pk=obj.pk).update(
                artifact_uuid_id=apps.get_model(
                    "django_eventspipe", "Artifact"
                ).objects.only("uuid").get(pk=obj.artifact_id).uuid
            )

    for obj in Pipeline.objects.only("pk", "definition_id").iterator():
        if obj.definition_id is not None:
            Pipeline.objects.filter(pk=obj.pk).update(
                definition_uuid_id=apps.get_model(
                    "django_eventspipe", "PipelineDefinition"
                ).objects.only("uuid").get(pk=obj.definition_id).uuid
            )

    for obj in Task.objects.only("pk", "definition_id").iterator():
        if obj.definition_id is not None:
            Task.objects.filter(pk=obj.pk).update(
                definition_uuid_id=apps.get_model(
                    "django_eventspipe",
                    "PipelineDefinitionTaskDefinition",
                ).objects.only("uuid").get(pk=obj.definition_id).uuid
            )

    for obj in PipelineDefinitionTaskDefinition.objects.only(
        "pk", "pipeline_definition_id"
    ).iterator():
        PipelineDefinitionTaskDefinition.objects.filter(
            pk=obj.pk
        ).update(
            pipeline_definition_uuid_id=apps.get_model(
                "django_eventspipe", "PipelineDefinition"
            ).objects.only("uuid").get(
                pk=obj.pipeline_definition_id
            ).uuid
        )


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0018_add_uuid_foreign_keys"),
    ]

    operations = [
        migrations.RunPython(
            populate_uuid_foreign_keys,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
