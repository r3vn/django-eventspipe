from celery import chain

from django.db import models
from django.apps import apps
from django.utils.module_loading import import_string

class PipelineDefinition(models.Model):

    rules   = models.JSONField(blank=True, null=True, default=dict)
    options = models.JSONField(blank=True, null=True, default=dict)
    enabled = models.BooleanField(default=True)

    @classmethod
    def get_definitions(cls, event: dict[str, object]) -> list[object]:
        """
        Get pipeline definitions for a given event, ensuring all filter values match.
        
        This method implements best-match filtering by returning only the definitions
        where all filters match the corresponding event data (AND condition).
        Definitions with fewer matches are excluded if higher-matching ones exist.
        """
        all_definitions = cls.objects.filter(enabled=True)

        matching_definitions = []

        max_matches = 0

        for definition in all_definitions:
            rules = definition.rules
            
            # If filters are present, ensure all conditions match
            if rules:
                match = all(event.get(key) == value for key, value in rules.items() if key in event)
                
                # Count the number of matching filters (AND condition)
                match_count = sum(1 for key, value in rules.items() if event.get(key) == value)
                
                # Only consider definitions where all filter conditions match
                if match:
                    if match_count > max_matches:
                        max_matches = match_count
                        matching_definitions = [definition]
                    elif match_count == max_matches:
                        matching_definitions.append(definition)
            else:
                # Generic definitions with no filters
                if max_matches == 0:
                    matching_definitions.append(definition)

        return matching_definitions


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
