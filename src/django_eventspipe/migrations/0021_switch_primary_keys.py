import uuid

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0020_enforce_uuid_foreign_keys"),
    ]

    operations = [
        # Remove old integer foreign keys.
        migrations.RemoveField(
            model_name="pipelineartifact",
            name="artifact",
        ),
        migrations.RemoveField(
            model_name="pipeline",
            name="definition",
        ),
        migrations.RemoveField(
            model_name="task",
            name="definition",
        ),
        migrations.RemoveField(
            model_name="pipelinedefinitiontaskdefinition",
            name="pipeline_definition",
        ),

        # Rename temporary UUID foreign keys.
        migrations.RenameField(
            model_name="pipelineartifact",
            old_name="artifact_uuid",
            new_name="artifact",
        ),
        migrations.RenameField(
            model_name="pipeline",
            old_name="definition_uuid",
            new_name="definition",
        ),
        migrations.RenameField(
            model_name="task",
            old_name="definition_uuid",
            new_name="definition",
        ),
        migrations.RenameField(
            model_name="pipelinedefinitiontaskdefinition",
            old_name="pipeline_definition_uuid",
            new_name="pipeline_definition",
        ),

        # Temporarily remove FK constraints to UUID unique indexes.
        # Keep the UUID columns and their data intact.

        migrations.AlterField(
            model_name="pipelineartifact",
            name="artifact",
            field=models.ForeignKey(
                to="django_eventspipe.artifact",
                to_field="uuid",
                db_constraint=False,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),

        migrations.AlterField(
            model_name="pipeline",
            name="definition",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinition",
                to_field="uuid",
                db_constraint=False,
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
            ),
        ),

        migrations.AlterField(
            model_name="task",
            name="definition",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinitiontaskdefinition",
                to_field="uuid",
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
            ),
        ),

        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="pipeline_definition",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinition",
                to_field="uuid",
                db_constraint=False,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),

        # Remove old integer primary keys.
        migrations.RemoveField(
            model_name="pipelineartifact",
            name="id",
        ),
        migrations.RemoveField(
            model_name="artifact",
            name="id",
        ),
        migrations.RemoveField(
            model_name="pipelinedefinition",
            name="id",
        ),
        migrations.RemoveField(
            model_name="pipelinedefinitiontaskdefinition",
            name="id",
        ),

        # Promote UUID fields to primary keys.
        migrations.AlterField(
            model_name="pipelineartifact",
            name="uuid",
            field=models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="uuid",
            field=models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="pipelinedefinition",
            name="uuid",
            field=models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="uuid",
            field=models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False,
                serialize=False,
            ),
        ),

        # Restore final foreign keys after the referenced models
        # have UUID primary keys in migration state.
        migrations.AlterField(
            model_name="pipelineartifact",
            name="artifact",
            field=models.ForeignKey(
                to="django_eventspipe.artifact",
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
        migrations.AlterField(
            model_name="pipeline",
            name="definition",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinition",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="definition",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinitiontaskdefinition",
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pipelinedefinitiontaskdefinition",
            name="pipeline_definition",
            field=models.ForeignKey(
                to="django_eventspipe.pipelinedefinition",
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]
