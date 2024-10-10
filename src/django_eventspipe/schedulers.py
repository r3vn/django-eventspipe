import logging

from celery.beat import Scheduler
from .models import EventSchedule

logger = logging.getLogger(__name__)

class DynamicScheduler(Scheduler):

    def __init__(self, app, *args, **kwargs) -> None:
        """
        Initialize the scheduler and set up the schedule.
        """
        super().__init__(app, *args, **kwargs)
        self.current_hash = None
        self.sync()  # Initialize the schedule on startup

    def sync(self) -> None:
        """
        Sync the schedule.
        """
        logger.info("Updating schedule from database...")

        # Compute the new schedule hash
        new_hash = EventSchedule.compute_hash()

        # If the schedule hasn't changed, skip the update
        if new_hash == self.current_hash:
            logger.info("No changes detected in schedule.")
            return

        # Fetch enabled schedules from the database
        schedules = EventSchedule.objects.filter(enabled=True)

        # Loop through schedules and update only changed or new entries
        for schedule in schedules:
            if schedule.entry_name not in self.schedule:
                # Add a new schedule entry
                self.schedule[schedule.entry_name] = schedule.entry
                logger.info(f"Added new task: {schedule.entry_name}")

            else:
                # Check if the existing task needs to be updated
                existing_task = self.schedule[schedule.entry_name]
                if existing_task.schedule != schedule.schedule:
                    self.schedule[schedule.entry_name] = schedule.entry
                    logger.info(f"Updated existing task: {schedule.entry_name}")

        # Remove tasks that are no longer present in the database
        current_task_ids = {s.entry_name for s in schedules}
        to_remove = [task_id for task_id in self.schedule if task_id not in current_task_ids]

        for task_id in to_remove:
            del self.schedule[task_id]
            logger.info(f"Removed task: {task_id}")

        # Update the current hash and last update time
        self.current_hash = new_hash
