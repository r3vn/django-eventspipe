from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0021_switch_primary_keys"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskdefinition",
            name="uuid",
            field=models.UUIDField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name="eventschedule",
            name="uuid",
            field=models.UUIDField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name="pipelinedefinitiontaskdefinition",
            name="task_definition_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.taskdefinition",
                to_field="uuid",
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                db_constraint=False,
            ),
        ),
    ]
