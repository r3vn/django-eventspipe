import traceback
import platform

from functools import wraps

from .models import Pipeline, Task
from .exceptions import TaskFailed

def tracked_task(func):
    @wraps(func)
    def wrapper(self, context: dict[str, object], *args, **kw) -> dict[str, object]:
        
        # HACK: Get task name
        if str(func.__name__) in str(func.__module__):
            taskname = str(func.__module__)
        else:
            taskname = "%s.%s" % (func.__module__, func.__name__)

        # Get Pipeline object
        self.pipeline = Pipeline.objects.get(pk=context["pipeline"])

        self.context = context
        
        # Get current pipeline's task
        pipeline_task = Task.objects.get(
            pipeline=self.pipeline, 
            definition__task_definition__function=taskname
        )

        self.pipeline.log("executing '%s'..." % taskname)

        # Start Task's tracking
        pipeline_task.tracking_start(node=platform.node())

        try:
            # Execute Task
            func(self, *args, **kw)

            # Set Task's status as success
            pipeline_task.tracking_update(1)

        except Exception as E:
            # Log the Exception
            self.pipeline.log(str(traceback.format_exc()))

            # Set Task's status as failed
            pipeline_task.tracking_update(2)

            raise TaskFailed

        self.pipeline.log("'%s' execution complete." % taskname)

        return self.context

    return wrapper
