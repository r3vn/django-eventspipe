from django.db import models

class PipelineDefinitionTaskDefinition(models.Model):
    pipeline_definition = models.ForeignKey('django_eventspipe.PipelineDefinition', on_delete=models.CASCADE)
    task_definition     = models.ForeignKey('django_eventspipe.TaskDefinition', on_delete=models.CASCADE)
    enabled             = models.BooleanField(default=True)
    order               = models.IntegerField(default=20)

