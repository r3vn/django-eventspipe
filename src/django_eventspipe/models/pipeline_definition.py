from celery import chain

from django.db import models
from django.apps import apps
from django.utils.module_loading import import_string

class PipelineDefinition(models.Model):
    event     = models.CharField(max_length=256)
    filters   = models.JSONField(blank=True, null=True, default=dict)
    options   = models.JSONField(blank=True, null=True, default=dict)
    enabled   = models.BooleanField(default=True)

    @classmethod
    def get_definitions(cls, event: dict[str, object]) -> list[object]:
        """
        Get pipeline definitions for a given event.
        """
        all_definitions = cls.objects.filter(event=event["name"], enabled=True)

        # Separate generic and custom definitions
        generic_definitions = []
        custom_definitions = []

        for definition in all_definitions:
            filters = definition.filters or {}
            
            # Check if filters exist, otherwise it's a generic definition
            if filters:
                match = all(
                    event.get(key) == value 
                    for key, value in filters.items()
                    if key in event
                )
                if match:
                    custom_definitions.append(definition)
            else:
                generic_definitions.append(definition)

        # Return custom definitions if available, otherwise return generic ones
        return custom_definitions if custom_definitions else generic_definitions

    @property
    def defined_tasks(self) -> list[object]:
        """
        Get Tasks defined for this PipelineDefinition
        """
        PipelineDefinitionTaskDefinition = apps.get_model('django_eventspipe.PipelineDefinitionTaskDefinition')

        tasks = []

        for definition in PipelineDefinitionTaskDefinition.objects.filter(
            pipeline_definition=self, 
            enabled=True
        ).order_by('order'):
            tasks.append(definition)

        return tasks

    def get_tasks_chain(self, context: dict[str, object]) -> chain:
        """
        Get Tasks defined for this PipelineDefinition as a celery chain
        """
        task_chain = []
        first = True

        for definition in self.defined_tasks:
            if first:
                signature = import_string(definition.task_definition.function).s(context)
                first = False
            else:
                signature = import_string(definition.task_definition.function).s()

            task_chain.append(signature)

        return chain(task_chain)
