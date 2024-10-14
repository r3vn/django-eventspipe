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
        This method implements best-match filtering by returning only the definitions
        with the highest number of matching rules. Definitions with fewer matches
        are excluded if a higher-matching one exists.
        """
        all_definitions = cls.objects.filter(enabled=True)
        matching_definitions = []
        max_matches = 0

        for definition in all_definitions:
            rules = definition.rules or {}
            match_count = 0
            
            # Count the number of matching rules
            for key, value in rules.items():
                if key in event and event[key] == value:
                    match_count += 1

            # If no rules, consider it a generic definition
            if match_count > 0:
                if match_count > max_matches:
                    max_matches = match_count
                    matching_definitions = [definition]
                elif match_count == max_matches:
                    matching_definitions.append(definition)
            else:
                # For generic definitions, if no custom ones are better
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
