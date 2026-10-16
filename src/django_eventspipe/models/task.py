from django.db import models
from django.utils import timezone


class TaskManager(models.Manager):

    def create_tasks(self, pipeline: object) -> list:
        """
        Create Tasks for a given pipeline.
        """
        tasks = []

        for defined_task in pipeline.definition.defined_tasks:
            task = self.create(
                status=3,
                pipeline=pipeline,
                definition=defined_task,
            )
            tasks.append(task)

        return tasks

    def pipeline_failed(self, pipeline: object) -> None:
        """
        Set all queued Tasks as failed.
        """
        self.filter(
            status=3,
            pipeline=pipeline,
        ).update(status=2)


class Task(models.Model):

    STATUS_CHOICES = [
        (0, "running"),
        (1, "success"),
        (2, "error"),
        (3, "queued"),
        (4, "skipped")
    ]

    status     = models.IntegerField(default=2, choices=STATUS_CHOICES)
    node       = models.CharField(max_length=256, default="undefined")
    pipeline   = models.ForeignKey('django_eventspipe.Pipeline', on_delete=models.CASCADE)
    definition = models.ForeignKey('django_eventspipe.PipelineDefinitionTaskDefinition', null=True, on_delete=models.SET_NULL)
    start_ts   = models.DateTimeField(blank=True, null=True)
    end_ts     = models.DateTimeField(blank=True, null=True)

    objects = TaskManager()

    def tracking_start(self, node: str) -> None:
        """
        Start tracking a `Task`
        """
        self.status = 0
        self.node = node
        self.start_ts = timezone.now()
        
        # Increase Pipeline's current_task
        self.pipeline.current_task += 1

        # Set Pipeline's status as running
        if self.pipeline.status != 0:
            self.pipeline.status = 0

        self.pipeline.save()
        self.save()

    def tracking_update(self, status: int) -> None:
        """
        Update `Task`'s tracking data
        """
        # Update this object
        self.status = status
        self.end_ts = timezone.now()

        if status == 1:
            # Check if pipeline is completed
            if self.pipeline.current_task == self.pipeline.tasks_count:
                self.pipeline.status = status
                self.pipeline.end_ts = timezone.now()
                self.pipeline.save()
        else:
            # Set pipeline and all queued Tasks as failed
            self.pipeline.fail()

        self.save()
