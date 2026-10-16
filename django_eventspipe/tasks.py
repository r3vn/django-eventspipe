from celery import shared_task

from .signals import event_signal
from .models import EventSchedule

@shared_task
def __trigger_event_schedule(schedule_pk: int) -> None:
    """
    This task trigger an event
    """
    schedule = EventSchedule.objects.get(pk=schedule_pk)
    event_signal.send(sender=schedule.user, event=schedule.event)
