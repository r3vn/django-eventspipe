from django.db import models
from django.apps import apps


class PipelineArtifactManager(models.Manager):

    def add_artifact(
        self, 
        pipeline: object, 
        file_name: str, 
        file_data: bytes
    ) -> bool:
        """
        Add a new artifact to the database
        """
        Artifact = apps.get_model("django_eventspipe.Artifact")

        artifact = Artifact.objects.get_or_create_artifact(file_data)

        pipeline_artifact = self.create(
            pipeline=pipeline,
            artifact=artifact,
            file_name=file_name
        )
        pipeline_artifact.save()

        return True

    def get_artifacts(self, pipeline: object) -> dict[str, object]:
        """
        Get stored artifacts for a Pipeline
        """
        out = {}
        artifacts = self.model.objects.filter(pipeline=pipeline)

        for artifact in artifacts:
            out[artifact.file_name] = bytes(artifact.artifact.data)

        return out
 

class PipelineArtifact(models.Model):
    """
    Artifact -> Pipeline association
    """
    file_name = models.CharField(max_length=1024, default="undefined")
    pipeline  = models.ForeignKey("django_eventspipe.Pipeline", on_delete=models.CASCADE)
    artifact  = models.ForeignKey("django_eventspipe.Artifact", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    objects = PipelineArtifactManager()

    class Meta:
        verbose_name = "Artifact"
        verbose_name_plural = "Artifacts"
