from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .utils import linkify, PrettyJSONEncoder

from .models import (
    PipelineDefinition,
    PipelineDefinitionTaskDefinition,
    Task,
    TaskDefinition,
    Pipeline,
    PipelineArtifact,
    EventSchedule
)

class InlineTask(admin.TabularInline):
    model = Task
    extra = 0
    ordering = ("pk",)
    can_delete = False
    readonly_fields = [
        '_status',
        '_name',
        'node',
        'start_ts',
        'end_ts'
    ]
    exclude = [
        'definition',
        'pipeline_definition',
        'status'
    ]

    def _status(self, obj):
        """
        Read job's status properly
        """
        colors = ["#2196F3","#04AA6D","#f23232", "#f8f8f8", "#ff9800"]
        return format_html(
            "<span style=\"background-color:%s;display:block;text-align:center;font-size:0.6rem;padding:1px;max-width:55px;\"><b>%s</b></span>" 
            % (
                colors[obj.status], 
                obj.get_status_display().upper()
            )
        )

    def _name(self, obj):
        return "%s" % obj.definition.task_definition.function

class JsonOptionsForm(forms.ModelForm):
    options = forms.JSONField(
        encoder=PrettyJSONEncoder,
        required=False
    )

class JsonEventForm(forms.ModelForm):
    event = forms.JSONField(
        encoder=PrettyJSONEncoder,
        required=False
    )

class InlineTaskDefinition(admin.TabularInline):
    model = PipelineDefinitionTaskDefinition
    extra = 0
    ordering = ("order",)
    exclude = ['options']

    def _name(self, obj):
        """
        Get Job function name from JobDefinition object
        """
        return "%s" % obj.task_definition.function


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "_status",
        "name",
        linkify("user"),
        "start_ts",
        "end_ts"
    )
    readonly_fields = []
    inlines = [InlineTask]

    # https://stackoverflow.com/a/19884095
    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def _status(self, obj):
        """
        Read job's status properly
        """
        colors = ["#2196F3","#04AA6D","#f23232", "#f8f8f8"]
        return format_html(
            "<span style=\"background-color:%s;display:block;text-align:center;font-size:0.6rem;padding:1px;max-width:55px;\"><b>%s</b></span>" 
            % (
                colors[obj.status], 
                obj.get_status_display().upper()
            )
        )

@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "enabled",
        "__str__",
        "user",
        "event",
    )
    form = JsonEventForm

    @admin.action(description="Disable selected EventSchedule")
    def disable_selection(self, request, queryset):
        for object in queryset:
            object.enabled = False
            object.save()

    @admin.action(description="Enable selected EventSchedule")
    def enable_selection(self, request, queryset):
        for object in queryset:
            object.enabled = True
            object.save()

    @admin.action(description="Duplicate selected EventSchedule")
    def duplicate_selection(self, request, queryset):
        for object in queryset:
            object.id = None
            object.save()

    actions = [duplicate_selection, enable_selection, disable_selection]

@admin.register(PipelineDefinition)
class PipelineDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "enabled",
        "event",
        "filters",
        "tasks_definition"
    )
    inlines = [InlineTaskDefinition]
    form = JsonOptionsForm

    @admin.action(description="Disable selected PipelineDefinition")
    def disable_selection(self, request, queryset):
        for object in queryset:
            object.enabled = False
            object.save()

    @admin.action(description="Enable selected PipelineDefinition")
    def enable_selection(self, request, queryset):
        for object in queryset:
            object.enabled = True
            object.save()

    @admin.action(description="Duplicate selected PipelineDefinition")
    def duplicate_selection(self, request, queryset):
        for object in queryset:

            task_definitions = PipelineDefinitionTaskDefinition.objects.filter(pipeline_definition=object)

            object.id = None
            object.save()

            for task_definition in task_definitions:
                task_definition.id = None
                task_definition.pipeline_definition = object
                task_definition.save()

    actions = [duplicate_selection, enable_selection, disable_selection]

    def tasks_definition(self, obj):
        """
        Return a "pretty" tasks execution order view 
        """
        rt_string = ""
        for definition in PipelineDefinitionTaskDefinition.objects.filter(pipeline_definition=obj).order_by('order'):
            if definition.enabled:
                job_name = definition.task_definition.function
            else:
                # task is disabled, Strikethrough the function name
                job_name = "<s style=\"color:var(--delete-button-bg)\">%s</s>" % definition.task_definition.function

            rt_string = "%s <span style=\"color:var(--link-fg)\">→</span> %s" % (rt_string, job_name)

        return format_html(rt_string)

@admin.register(TaskDefinition)
class TaskDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        "function",
        "description"
    )
    ordering = ('function',)

@admin.register(PipelineArtifact)
class PipelineArtifactAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "file_name",
        "_size",
        "artifact__md5sum",
        linkify("pipeline"),
        "timestamp",
        "download"
    )

    readonly_fields = []

    # https://stackoverflow.com/a/19884095
    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def download(self, obj: PipelineArtifact) -> str:
        url = reverse('get_artifact', args=(obj.pk,))
        return format_html("<a class='button' href='%s'>📝 DOWNLOAD</a>" % url)

    def _size(self, obj: PipelineArtifact) -> str:
        return "%s KB" % str(obj.artifact.size)
