from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0015_alter_pipelineartifact_pipeline_alter_task_pipeline"),
    ]

    operations = [
        migrations.AddField(
            model_name="pipelineartifact",
            name="uuid",
            field=models.UUIDField(
                null=True,
                editable=False,
            ),
        ),

        migrations.AddField(
            model_name="artifact",
            name="uuid",
            field=models.UUIDField(
                null=True,
                editable=False,
            ),
        ),

        migrations.AddField(
            model_name="pipelinedefinition",
            name="uuid",
            field=models.UUIDField(
                null=True,
                editable=False,
            ),
        ),

        migrations.AddField(
            model_name="pipelinedefinitiontaskdefinition",
            name="uuid",
            field=models.UUIDField(
                null=True,
                editable=False,
            ),
        ),
    ]
