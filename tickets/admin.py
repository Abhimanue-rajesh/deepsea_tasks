from django.contrib import admin, messages
from django.shortcuts import redirect
from unfold.admin import ModelAdmin

from tickets.models import SupportTicket, TicketRouting, TicketStatus


@admin.register(SupportTicket)
class SupportTicketAdmin(ModelAdmin):
    change_list_template = "tickets/change_list.html"

    list_display = (
        "ticket_number",
        "ticket_name",
        "routing",
        "completion_status",
        "raised_by",
        "last_updated_date",
    )

    list_filter = (
        "routing",
        "completion_status",
        "last_updated_date",
        "created_at",
    )

    search_fields = (
        "ticket_number",
        "ticket_name",
        "status_note",
        "raised_by",
    )

    autocomplete_fields = (
        "routing",
        "completion_status",
        "related_ticket",
    )

    readonly_fields = ("created_at",)

    ordering = (
        "-last_updated_date",
        "-ticket_number",
    )

    fieldsets = (
        (
            "Ticket Details",
            {
                "fields": (
                    "ticket_number",
                    "ticket_name",
                    "routing",
                    "completion_status",
                    "raised_by",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "last_updated_date",
                    "status_note",
                    "related_ticket",
                )
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST" and request.POST.get("_quick_add_ticket"):
            SupportTicket.objects.create(
                user=request.user,
                ticket_number=request.POST.get("ticket_number") or None,
                ticket_name=request.POST.get("ticket_name"),
                routing_id=request.POST.get("routing") or None,
                completion_status_id=request.POST.get("completion_status") or None,
                raised_by=request.POST.get("raised_by") or "Not Recorded",
            )

            messages.success(request, "Support ticket created successfully.")
            return redirect(request.path)

        extra_context = extra_context or {}
        extra_context["ticket_routings"] = TicketRouting.objects.all()
        extra_context["ticket_statuses"] = TicketStatus.objects.all()

        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)

        # Show closed tickets only when searched or filtered
        is_searching = bool(request.GET.get("q"))
        is_filtering = any(
            key for key in request.GET.keys() if key not in ["q", "p", "o", "e"]
        )

        if is_searching or is_filtering:
            return qs

        return qs.exclude(completion_status__name__iexact="Closed")


@admin.register(TicketRouting)
class TicketRoutingAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(TicketStatus)
class TicketStatusAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
