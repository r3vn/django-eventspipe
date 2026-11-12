import uuid

from django.db import migrations, models
import django.db.models.deletion


def populate_uuids(apps, schema_editor):
    TaskDefinition = apps.get_model(
        "django_eventspipe", "TaskDefinition"
    )
    EventSchedule = apps.get_model(
        "django_eventspipe", "EventSchedule"
    )
    PipelineDefinitionTaskDefinition = apps.get_model(
        "django_eventspipe", "PipelineDefinitionTaskDefinition"
    )

    for Model in (TaskDefinition, EventSchedule):
        for obj in Model.objects.filter(uuid__isnull=True).only("pk").iterator():
            Model.objects.filter(pk=obj.pk).update(uuid=uuid.uuid4())

    task_definition_uuids = dict(
        TaskDefinition.objects.values_list("pk", "uuid")
    )

    for obj in PipelineDefinitionTaskDefinition.objects.only(
        "pk", "task_definition_id"
    ).iterator():
        PipelineDefinitionTaskDefinition.objects.filter(pk=obj.pk).update(
            task_definition_uuid_id=task_definition_uuids[obj.task_definition_id]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0022_add_uuid_fields"),
    ]

    operations = [
        migrations.RunPython(
            populate_uuids,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="taskdefinition",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                unique=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="eventschedule",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                unique=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="task_definition_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.taskdefinition",
                to_field="uuid",
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]

