import platform

from django.apps import apps
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

from django_eventspipe.utils import get_sentinel_user

class Pipeline(models.Model):
    
    STATUS_CHOICES = [
        (0, "running"),
        (1, "success"),
        (2, "error"),
        (3, "queued")
    ]

    node         = models.CharField(max_length=256, default="undefined")
    name         = models.CharField(max_length=128)
    status       = models.IntegerField(default=3, choices=STATUS_CHOICES)
    definition   = models.ForeignKey('django_eventspipe.PipelineDefinition', on_delete=models.SET_NULL, blank=True, null=True)
    tasks_count  = models.IntegerField(default=0)
    current_task = models.IntegerField(default=0)
    start_ts     = models.DateTimeField(auto_now_add=True)
    end_ts       = models.DateTimeField(blank=True, null=True)
    user         = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))

    @classmethod
    def new_from_event(
        cls, 
        user: User, 
        event: dict[str, object]
    ) -> object | bool:
        """
        This function attempt to create and execute `Pipeline` objects from a event dictionary.
        `Pipeline` object require a `PipelineDefinition` object defined in order to start.
        Filtered `PipelineDefinition` objects always have priority over generic ones,
        this allow replacing definitions only when required. 
        """
        PipelineDefinition = apps.get_model("django_eventspipe.PipelineDefinition")

        # Check for available info for this event
        if "info" in event.keys():
            pipeline_name = "%s %s" % (event["name"], event["info"])
        else:
            pipeline_name = event["name"]

        # Create the pipeline objects
        pipelines   = []
        definitions = PipelineDefinition.get_definitions(event)

        if len(definitions) <= 0:
            # no such pipeline definition
            return False

        for definition in definitions:
            # Create Pipeline object
            pipeline = cls(
                name=pipeline_name, 
                user=user, 
                node=platform.node(),
                definition=definition
            )
            pipeline.save()

            # Run Pipeline
            pipeline.execute(event)
            pipelines.append(pipeline)

        return pipelines

    @property
    def __task_progress_str(self) -> str:
        if self.tasks_count > 0:
            return "[%d/%d]" % (self.current_task+1, self.tasks_count)
        else:
            return ""

    @property
    def artifacts(self) -> dict[str, object]:
        """
        Get stored artifacts for this Pipeline
        """
        PipelineArtifact = apps.get_model("django_eventspipe.PipelineArtifact")

        return PipelineArtifact.get_artifacts(self)

    def __str__(self) -> str:
        return "Pipeline #%d" % self.pk

    def save_artifact(self, file_name: str, file_data: bytes) -> bool:
        """
        Save an artifact for this Pipeline
        """
        PipelineArtifact = apps.get_model("django_eventspipe.PipelineArtifact")

        return PipelineArtifact.add_artifact(
            pipeline  = self,
            file_name = file_name, 
            file_data = file_data,
        )

    def execute(self, event: dict[str, object]) -> None:
        """ 
        Execute a `Pipeline`
        """
        Task = apps.get_model("django_eventspipe.Task")

        # add initial pipeline's log entry
        self.log("Event received %s" % str(event))

        # Get initial context from event
        context = {
            "pipeline" : self.pk
        }

        # retrive context data from event
        for data in event.keys():
            context[data] = event[data]

        # retrive context data from PipelineDefinitinon's options
        for data in self.definition.options.keys():
            context[data] = self.definition.options[data]

        # Get Task definition for this event on this perimeter
        pipeline_tasks   = Task.create_tasks(self)

        # No Tasks defined for this pipeline, exit
        if len(pipeline_tasks) <= 0:
            self.status = 1
            self.tasks_count = 0
            self.current_task = 0
            self.end_ts = timezone.now()
            self.save()

            return None

        # Set pipeline as queued
        self.status      = 3
        self.tasks_count = len(pipeline_tasks)
        self.save()

        # Get and start celery chain for this pipeline
        pipeline_chain = self.definition.get_tasks_chain(context) 
        pipeline_chain.apply_async()

    def log(self, entry: str) -> None:
        """
        Add a LogEntry on a `Pipeline`
        """
        log_entry = "%s%s" % (self.__task_progress_str, entry)

        # Add an ADDITION logentry for this asset
        LogEntry.objects.log_action(
            user_id=self.user.pk,
            content_type_id=ContentType.objects.get_for_model(Pipeline).pk,
            object_id=self.id,
            object_repr="Pipeline #%d" % self.id,
            action_flag=ADDITION,
            change_message=log_entry
        )

    def fail(self) -> None:
        """
        Set a `Pipeline` and his uncompleted `Task` objects as failed.
        """
        Task = apps.get_model("django_eventspipe.Task")

        # Update Pipeline object
        self.status = 2
        self.end_ts = timezone.now()
        self.save()

        # Update queued Tasks
        Task.pipeline_failed(self)
