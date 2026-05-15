from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.timezone import localdate


class TaskCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY = [
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    STATUS = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("terminated", "Terminated"),
        ("waiting_for_approval", "Waiting For Approval"),
        ("completed", "Completed"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=27, choices=STATUS, default="not_started")
    priority = models.CharField(max_length=27, choices=PRIORITY)

    category = models.ForeignKey(
        TaskCategory, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_date = models.DateField(auto_now=True)
    due_date = models.DateField(default=localdate)

    submitted_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_view_approved_tasks", "Can View Approved Tasks"),
            ("can_view_submitted_tasks", "Can View Submitted Tasks"),
        ]
        ordering = ["created_at"]

    def __str__(self):
        return self.title

    def days_left(self):
        if not self.due_date:
            return None

        today = timezone.localdate()

        due_date = self.due_date

        # convert datetime to date if needed
        if hasattr(due_date, "date"):
            due_date = due_date.date()

        return (due_date - today).days

    # 🔹 Helper: get next pending step in the action plan
    def next_action_step(self):
        return (
            self.action_steps.filter(status__in=["pending", "in_progress"])
            .order_by("order", "due_date")
            .first()
        )

    # 🔹 Helper: check if there are any open steps
    def has_open_action_steps(self):
        return self.action_steps.exclude(status="completed").exists()

    def is_overdue(self):
        days = self.days_left()
        return days is not None and days < 0

    def deadline(self):
        """
        Human-friendly text for the email.
        """
        days = self.days_left()
        if days is None:
            return "No due date set"
        if days < 0:
            return f"Overdue by {abs(days)} day(s)"
        if days == 0:
            return "Due today"
        if days == 1:
            return "Due in 1 day"
        return f"Due in {days} days"


class TaskActionStep(models.Model):
    """
    A detailed action plan step for a Task.

    Example usage:
    - “Create draft PPT”
    - “Get approval from manager”
    - “Share with Insight team”
    """

    STATUS = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("blocked", "Blocked"),
        ("completed", "Completed"),
    ]

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="action_steps",
    )
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending",
    )

    assigned_to = models.CharField(max_length=200)

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateField(null=True, blank=True)
    completed_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["order", "due_date", "id"]

    def __str__(self):
        return f"{self.task.title} - {self.title}"

    def mark_completed(self):
        self.status = "completed"
        self.completed_at = timezone.now()
        self.save()
