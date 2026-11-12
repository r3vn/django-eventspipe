from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_eventspipe", "0012_populate_uuid_foreign_keys"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="pipeline_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipeline",
                to_field="uuid",
                db_column="pipeline_uuid_id",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
            ),
        ),

        migrations.AlterField(
            model_name="pipelineartifact",
            name="pipeline_uuid",
            field=models.ForeignKey(
                to="django_eventspipe.pipeline",
                to_field="uuid",
                db_column="pipeline_uuid_id",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
            ),
        ),
    ]
