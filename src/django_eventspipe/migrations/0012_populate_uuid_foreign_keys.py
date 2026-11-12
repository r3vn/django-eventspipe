from django.db import migrations


def populate_pipeline_foreign_keys(apps, schema_editor):

    Task = apps.get_model("django_eventspipe", "Task")
    PipelineArtifact = apps.get_model(
        "django_eventspipe",
        "PipelineArtifact",
    )

    db = schema_editor.connection.alias

    # Migrate Task.pipeline
    tasks = (
        Task.objects.using(db)
        .select_related("pipeline")
        .iterator(chunk_size=2000)
    )

    for task in tasks:
        task.pipeline_uuid_id = task.pipeline.uuid
        task.save(
            update_fields=["pipeline_uuid"],
            using=db,
        )

    # Migrate PipelineArtifact.pipeline
    artifacts = (
        PipelineArtifact.objects.using(db)
        .select_related("pipeline")
        .iterator(chunk_size=2000)
    )

    for artifact in artifacts:
        artifact.pipeline_uuid_id = artifact.pipeline.uuid
        artifact.save(
            update_fields=["pipeline_uuid"],
            using=db,
        )


class Migration(migrations.Migration):

    atomic = True

    dependencies = [
        ("django_eventspipe", "0011_add_uuid_foreign_keys"),
    ]

    operations = [
        migrations.RunPython(
            populate_pipeline_foreign_keys,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
