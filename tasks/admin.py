from django.contrib import admin, messages

# from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import localdate
from unfold.admin import ModelAdmin, StackedInline
from unfold.decorators import display

from .models import Task, TaskActionStep, TaskActivity, TaskCategory

# admin.site.unregister(Group)


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


class TaskActivityAdmin(StackedInline):
    model = TaskActivity
    extra = 0


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    change_list_template = "tasks/change_list.html"
    list_display = (
        "title",
        "priority",
        "status",
        "last_activity_display",
        "last_activity_date_display",
        "due_date",
        "pending_with",
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
    )
    list_editable = ("status",)
    autocomplete_fields = ("category",)
    readonly_fields = (
        "created_at",
        "updated_date",
        "submitted_date",
        "days_left",
        "is_overdue",
        "deadline",
    )
    inlines = [
        TaskActivityAdmin,
        TaskActionStepInline,
    ]
    ordering = ("created_at",)

    fieldsets = (
        (
            "Task Details",
            {
                "fields": (
                    "title",
                    "description",
                    "category",
                    "priority",
                    "status",
                    "pending_with",
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

    class Media:
        js = (
            "js/task_autosave.js",
            "js/admin_row_click.js",
        )

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

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST" and request.POST.get("_quick_add_task") == "1":
            title = request.POST.get("title")
            priority = request.POST.get("priority")
            due_date = request.POST.get("due_date") or localdate()
            status = request.POST.get("status") or "not_started"
            category_id = request.POST.get("category")

            if not title or not priority or not due_date:
                messages.error(request, "Please fill all required fields.")
                return redirect(request.path)

            task = Task(
                user=request.user,
                title=title,
                priority=priority,
                due_date=due_date,
                status=status,
            )

            if category_id:
                task.category_id = category_id

            task.save()

            messages.success(request, "Task added successfully.")
            # return redirect(reverse("admin:tasks_task_change", args=[task.pk]))

        extra_context = extra_context or {}
        extra_context["task_categories"] = TaskCategory.objects.all()
        extra_context["task_priorities"] = Task.PRIORITY
        extra_context["task_statuses"] = Task.STATUS
        extra_context["today"] = localdate()

        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user

        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse("admin:tasks_task_change", args=[obj.pk]))

    def response_change(self, request, obj):
        return redirect(reverse("admin:tasks_task_change", args=[obj.pk]))

    @admin.display(description="Last Activity")
    def last_activity_display(self, obj):
        activity = obj.last_activity()

        if not activity:
            return "-"

        return activity.activity_note

    @admin.display(description="Last Activity Date")
    def last_activity_date_display(self, obj):
        return obj.last_activity_date() or "-"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # If status filter is selected, allow Django filter to work normally
        if "status__exact" in request.GET:
            return queryset

        # Default view: hide closed tasks
        return queryset.exclude(status="closed")


@admin.register(TaskCategory)
class TaskCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    class Media:
        js = ("js/admin_row_click.js",)
