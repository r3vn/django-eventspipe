from django.db import models
from django.utils.module_loading import import_string


class TaskDefinitionManager(models.Manager):
    
    def check_definitions(self, tasks: list) -> None:
        """
        Automatically import `Task` objects from celery
        """
        clean_tasks = []

        # skip celery stuff
        for task in tasks:
            if "celery." in task or "django_eventspipe." in task:
                continue
            clean_tasks.append(task)

        # remove uknown `TaskDefinition`
        for taskdef in self.model.objects.all():
            if taskdef.function not in clean_tasks:
                taskdef.delete()

        # import registered `Task` objects
        for task in clean_tasks:
            try:
                imported_task = import_string(task)

                if not self.model.objects.filter(function=task).exists():
                    # Get `Task` function and documentation
                    new_task_def = self.model(
                        function=task,
                        description=imported_task.__doc__
                    )
                    new_task_def.save()

            except: pass


class TaskDefinition(models.Model):

    function    = models.CharField(max_length=512, unique=True)
    description = models.TextField(null=True, blank=True)

    objects = TaskDefinitionManager()

    def __str__(self) -> str:
        return "%s" % self.function
