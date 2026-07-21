from django.contrib import admin, messages

# from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.timezone import localdate
from django.views.generic import TemplateView
from unfold.admin import ModelAdmin, StackedInline
from unfold.decorators import display
from unfold.views import UnfoldModelAdminViewMixin

from tasks.models import Project, Task, TaskActionStep, TaskActivity, TaskCategory

# from django.db.models import Count


class TasksDashboard(UnfoldModelAdminViewMixin, TemplateView):
    title = "Task Dashboard"
    permission_required = ()
    template_name = "tasks/tasks_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["projects"] = Project.objects.all().order_by("name")
        context["task_list_url"] = reverse("admin:tasks_task_changelist")

        return context


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
        "project",
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
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Task Details",
            {
                "fields": (
                    "project",
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

    def get_urls(self):
        custom_urls = [
            path(
                "dashboard/",
                self.admin_site.admin_view(TasksDashboard.as_view(model_admin=self)),
                name="tasks_dashboard",
            ),
        ]

        return custom_urls + super().get_urls()


@admin.register(TaskCategory)
class TaskCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    class Media:
        js = ("js/admin_row_click.js",)


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    class Media:
        js = ("js/admin_row_click.js",)
