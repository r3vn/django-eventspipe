import uuid

from django.db import models
from django.utils.module_loading import import_string

class TaskDefinition(models.Model):
    uuid        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    function    = models.CharField(max_length=512, unique=True)
    description = models.TextField(null=True, blank=True)

    @classmethod
    def check_definitions(cls, tasks: list) -> None:
        """
        Automatically import `Task` objects from celery
        """
        clean_tasks = []

        # skip celery stuff
        for task in tasks:
            if "celery." in task or "django_eventspipe." in task: continue
            clean_tasks.append(task)

        # remove uknown `TaskDefinition`
        for taskdef in cls.objects.all():
            if taskdef.function not in clean_tasks:
                taskdef.delete()

        # import registered `Task` objects
        for task in clean_tasks:
            try:
                imported_task = import_string(task)

                if not cls.objects.filter(function=task).exists():
                    # Get `Task` function and documentation
                    new_task_def = cls(
                        function=task, 
                        description=imported_task.__doc__
                    )
                    new_task_def.save()
            except: pass

    def __str__(self) -> str:
        return "%s" % self.function
