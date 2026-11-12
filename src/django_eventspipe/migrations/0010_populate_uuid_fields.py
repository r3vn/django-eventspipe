import uuid

from django.db import migrations, models


def populate_uuids(apps, schema_editor):
    Pipeline = apps.get_model("django_eventspipe", "Pipeline")
    Task = apps.get_model("django_eventspipe", "Task")

    db = schema_editor.connection.alias

    for Model in (Pipeline, Task):
        queryset = (
            Model.objects.using(db)
            .filter(uuid__isnull=True)
            .only("pk")
        )

        for obj in queryset.iterator(chunk_size=2000):
            obj.uuid = uuid.uuid4()
            obj.save(update_fields=["uuid"], using=db)


class Migration(migrations.Migration):

    atomic = True

    dependencies = [
        ("django_eventspipe", "0009_add_uuid_fields"),
    ]

    operations = [
        migrations.RunPython(
            populate_uuids,
            reverse_code=migrations.RunPython.noop,
        ),

        migrations.AlterField(
            model_name="pipeline",
            name="uuid",
            field=models.UUIDField(
                unique=True,
                null=False,
                editable=False,
            ),
        ),

        migrations.AlterField(
            model_name="task",
            name="uuid",
            field=models.UUIDField(
                unique=True,
                null=False,
                editable=False,
            ),
        ),
    ]
