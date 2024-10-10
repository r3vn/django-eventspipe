import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone

from celery import schedules
from celery.beat import ScheduleEntry

from django_eventspipe import validators
from django_eventspipe.utils import cronexp, get_sentinel_user

class EventSchedule(models.Model):

    event = models.JSONField(
        default    = dict, 
        validators = [validators.event_validator],
        help_text  = 'Initial context for a Pipeline'
    )
    user     = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    enabled  = models.BooleanField(default=False)
    minute   = models.CharField(
        max_length   = 60 * 4, 
        default      = '*',
        verbose_name = 'Minute(s)',
        help_text    = 'Cron Minutes to Run. Use "*" for "all". (Example: "0,30")',
        validators   = [validators.minute_validator],
    )
    hour = models.CharField(
        max_length   = 24 * 4, 
        default      = '*',
        verbose_name = 'Hour(s)',
        help_text    = 'Cron Hours to Run. Use "*" for "all". (Example: "8,20")',
        validators   = [validators.hour_validator],
    )
    day_of_month = models.CharField(
        max_length   = 31 * 4, 
        default      = '*',
        verbose_name = 'Day(s) Of The Month',
        help_text    = 'Cron Days Of The Month to Run. Use "*" for "all". (Example: "1,15")',
        validators   = [validators.day_of_month_validator],
    )
    month_of_year = models.CharField(
        max_length   = 64, 
        default      = '*',
        verbose_name = 'Month(s) Of The Year',
        help_text    = 'Cron Months (1-12) Of The Year to Run. Use "*" for "all". (Example: "1,12")',
        validators   = [validators.month_of_year_validator],
    )
    day_of_week = models.CharField(
        max_length   = 64, 
        default      = '*',
        verbose_name = 'Day(s) Of The Week',
        help_text    = 'Cron Days Of The Week to Run. Use "*" for "all", Sunday is 0 or 7, Monday is 1. (Example: "0,5")',
        validators   = [validators.day_of_week_validator],
    )

    @classmethod
    def compute_hash(cls) -> str:
        """
        Compute a hash of the enabled schedules to detect changes.
        """
        schedules = cls.objects.filter(enabled=True)
        schedule_str = ''.join(
            f"{s.pk}-{s.__str__}" 
            for s in schedules
        )
        return hashlib.md5(schedule_str.encode()).hexdigest()

    def __str__(self) -> str:
        return '{} {} {} {} {} ({})'.format(
            cronexp(self.minute), cronexp(self.hour),
            cronexp(self.day_of_month), cronexp(self.month_of_year),
            cronexp(self.day_of_week), str(get_current_timezone())
        )

    @property
    def entry_name(self) -> str:
        """
        Return "schedule-{schedule.pk}" key
        """
        return "schedule-%d" % self.pk

    @property
    def entry(self) -> ScheduleEntry:
        """
        Get a celery's ScheduleEntry for an EventSchedule object
        """
        return ScheduleEntry(
            name     = self.entry_name,
            schedule = self.schedule,
            task     = 'django_eventspipe.tasks.__trigger_event_schedule',
            args     = [self.pk],
        )

    @property
    def schedule(self) -> schedules.crontab:
        """
        Get crontab schedules for an EventSchedule object
        """
        crontab = schedules.crontab(
            minute        = self.minute,
            hour          = self.hour,
            day_of_week   = self.day_of_week,
            day_of_month  = self.day_of_month,
            month_of_year = self.month_of_year,
        )
        return crontab
