from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin, StackedInline
from unfold.decorators import display

from .models import Task, TaskActionStep, TaskCategory

admin.site.unregister(Group)


class TaskActionStepInline(StackedInline):
    model = TaskActionStep
    extra = 0
    fields = (
        "order",
        "title",
        "status",
        "due_date",
        "started_at",
        "completed_at",
    )


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_display = (
        "title",
        "user",
        "status_badge",
        "priority_badge",
        "category",
        "due_date",
        "days_left",
    )
    list_filter = (
        "status",
        "priority",
        "category",
        "due_date",
    )
    search_fields = (
        "title",
        "description",
        "user__username",
        "user__email",
    )
    autocomplete_fields = ("user", "category")
    readonly_fields = (
        "created_at",
        "updated_date",
        "submitted_date",
        "days_left",
        "is_overdue",
        "deadline",
    )
    inlines = [TaskActionStepInline]
    ordering = ("created_at",)

    fieldsets = (
        (
            "Task Details",
            {
                "fields": (
                    "user",
                    "title",
                    "description",
                    "category",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    ("created_at", "updated_date"),
                    "due_date",
                    "days_left",
                    "is_overdue",
                    "deadline",
                )
            },
        ),
    )

    @display(
        description="Status",
        label={
            "not_started": "info",
            "in_progress": "warning",
            "terminated": "danger",
            "waiting_for_approval": "warning",
            "completed": "success",
            "closed": "success",
        },
    )
    def status_badge(self, obj):
        return obj.status

    @display(
        description="Priority",
        label={
            "critical": "danger",
            "high": "warning",
            "medium": "info",
            "low": "success",
        },
    )
    def priority_badge(self, obj):
        return obj.priority


@admin.register(TaskCategory)
class TaskCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
