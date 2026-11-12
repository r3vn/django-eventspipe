from django.db import models
from .base import UUID4Model


class PipelineDefinitionTaskDefinition(UUID4Model):

    pipeline_definition = models.ForeignKey('django_eventspipe.PipelineDefinition', on_delete=models.CASCADE)
    task_definition     = models.ForeignKey('django_eventspipe.TaskDefinition', on_delete=models.CASCADE)
    enabled             = models.BooleanField(default=True)
    order               = models.IntegerField(default=20)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField('creation date', auto_now_add=True)

    def __str__(self) -> str:
        return "TaskDefinition #%s" % self.short_uuid
