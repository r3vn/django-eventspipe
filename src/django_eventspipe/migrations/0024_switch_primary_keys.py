import uuid

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0023_populate_uuid_fields"),
    ]

    operations = [
        # Remove the original integer FK.
        migrations.RemoveField(
            model_name="pipelinedefinitiontaskdefinition",
            name="task_definition",
        ),

        # Rename the UUID FK to the original field name.
        migrations.RenameField(
            model_name="pipelinedefinitiontaskdefinition",
            old_name="task_definition_uuid",
            new_name="task_definition",
        ),

        # Temporarily remove the FK constraint, keeping its UUID values.
        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="task_definition",
            field=models.ForeignKey(
                to="django_eventspipe.taskdefinition",
                to_field="uuid",
                db_constraint=False,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),

        # Remove old integer primary keys.
        migrations.RemoveField(
            model_name="taskdefinition",
            name="id",
        ),
        migrations.RemoveField(
            model_name="eventschedule",
            name="id",
        ),

        # Promote UUIDs to primary keys.
        migrations.AlterField(
            model_name="taskdefinition",
            name="uuid",
            field=models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="eventschedule",
            name="uuid",
            field=models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False,
                serialize=False,
            ),
        ),

        # Restore the FK constraint against the new UUID primary key.
        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="task_definition",
            field=models.ForeignKey(
                to="django_eventspipe.taskdefinition",
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]
