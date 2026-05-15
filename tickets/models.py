from django.conf import settings
from django.db import models
from django.utils import timezone


class TicketRouting(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TicketStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SupportTicket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="support_tickets",
    )

    ticket_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    ticket_name = models.CharField(max_length=255)

    routing = models.ForeignKey(
        TicketRouting,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    completion_status = models.ForeignKey(
        TicketStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    last_updated_date = models.DateField(
        null=True,
        blank=True,
    )

    status_note = models.TextField(blank=True)

    raised_by = models.CharField(
        max_length=100,
        blank=True,
    )

    related_ticket = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_tickets",
    )

    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = [
            "-last_updated_date",
            "-ticket_number",
        ]

    def __str__(self):
        if self.ticket_number:
            return f"{self.ticket_number} - {self.ticket_name}"
        return self.ticket_name

    def mark_updated(self):
        self.last_updated_date = timezone.localdate()
        self.save()
