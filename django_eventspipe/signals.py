import logging

from django.dispatch import Signal, receiver
from django.contrib.auth.models import User

from .models import Pipeline

logger = logging.getLogger(__name__)
event_signal = Signal()

@receiver(event_signal)
def create_pipelines(
    sender: User, 
    event: dict[str, object], 
    **kwargs
) -> None:
    """
    Signal handler to create `Pipeline` objects from an event
    """
    logger.info("executing '%s'" % str(event))
    Pipeline.objects.new_from_event(sender, event)

