from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    atomic = True

    dependencies = [
        ("django_eventspipe", "0013_enforce_uuid_foreign_keys"),
    ]

    operations = [

        # Remove the old integer foreign keys.
        migrations.RemoveField(
            model_name="task",
            name="pipeline",
        ),

        migrations.RemoveField(
            model_name="pipelineartifact",
            name="pipeline",
        ),

        # Rename the UUID foreign keys to their original field names.
        migrations.RenameField(
            model_name="task",
            old_name="pipeline_uuid",
            new_name="pipeline",
        ),

        migrations.RenameField(
            model_name="pipelineartifact",
            old_name="pipeline_uuid",
            new_name="pipeline",
        ),

        # Switch the physical PostgreSQL primary keys.
        migrations.SeparateDatabaseAndState(

            database_operations=[
                migrations.RunSQL(
                    sql="""
                        -- Pipeline primary key
                        ALTER TABLE django_eventspipe_pipeline
                            DROP CONSTRAINT django_eventspipe_pipeline_pkey;

                        ALTER TABLE django_eventspipe_pipeline
                            DROP COLUMN id;

                        ALTER TABLE django_eventspipe_pipeline
                            ADD CONSTRAINT django_eventspipe_pipeline_pkey
                            PRIMARY KEY (uuid);


                        -- Task primary key
                        ALTER TABLE django_eventspipe_task
                            DROP CONSTRAINT django_eventspipe_task_pkey;

                        ALTER TABLE django_eventspipe_task
                            DROP COLUMN id;

                        ALTER TABLE django_eventspipe_task
                            ADD CONSTRAINT django_eventspipe_task_pkey
                            PRIMARY KEY (uuid);
                    """,
                    reverse_sql=None,
                ),
            ],

            state_operations=[
                migrations.RemoveField(
                    model_name="pipeline",
                    name="id",
                ),

                migrations.AlterField(
                    model_name="pipeline",
                    name="uuid",
                    field=models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                    ),
                ),

                migrations.RemoveField(
                    model_name="task",
                    name="id",
                ),

                migrations.AlterField(
                    model_name="task",
                    name="uuid",
                    field=models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                    ),
                ),
            ],
        ),
    ]
