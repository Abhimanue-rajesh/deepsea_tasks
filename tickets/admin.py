from django.contrib import admin, messages
from django.shortcuts import redirect
from unfold.admin import ModelAdmin

from quickcopy.models import QuickCopy
from tickets.models import SupportTicket, TicketRouting, TicketStatus


@admin.register(SupportTicket)
class SupportTicketAdmin(ModelAdmin):
    change_list_template = "tickets/change_list.html"
    list_display = (
        "ticket_number",
        "ticket_name",
        "status",
        "is_urgent",
        "updated_on",
    )
    list_filter = (
        "routing",
        "status",
        "created_at",
    )
    list_editable = ("status",)
    search_fields = (
        "ticket_number",
        "ticket_name",
        "status_note",
        "raised_by",
    )
    autocomplete_fields = (
        "routing",
        "status",
        "related_ticket",
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Ticket Details",
            {
                "fields": (
                    "ticket_number",
                    "ticket_name",
                    "routing",
                    "raised_by",
                    "is_urgent",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "last_updated_date",
                    "status_note",
                    "related_ticket",
                    "created_at",
                )
            },
        ),
    )

    @admin.display(description="Updated")
    def updated_on(self, obj):
        return obj.last_updated_date

    @admin.display(description="Created")
    def created_on(self, obj):
        return obj.created_at

    class Media:
        css = {"all": ("css/ticket_admin.css",)}
        js = (
            "js/admin_row_click.js",
            "quickcopy/js/quickcopy.js",  # This is needed for the ticket related quick copy functionality
        )

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST" and request.POST.get("_quick_add_ticket"):
            ticket_number = request.POST.get("ticket_number")
            SupportTicket.objects.create(
                user=request.user,
                ticket_number=ticket_number.strip() if ticket_number else None,
                ticket_name=request.POST.get("ticket_name"),
                routing_id=request.POST.get("routing") or None,
                status_id=request.POST.get("status") or None,
                raised_by=request.POST.get("raised_by") or "Not Recorded",
            )

            messages.success(request, "Support ticket created successfully.")
            return redirect(request.path)

        extra_context = extra_context or {}
        extra_context["ticket_routings"] = TicketRouting.objects.all()
        extra_context["ticket_statuses"] = TicketStatus.objects.all()
        extra_context["quick_copy_items"] = QuickCopy.objects.filter(
            related_to_tickets=True
        ).order_by("title")

        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.ticket_number = (
            str(obj.ticket_number).strip() if obj.ticket_number else None
        )
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.GET:
            return queryset

        return queryset.exclude(status__name__iexact="Closed")


@admin.register(TicketRouting)
class TicketRoutingAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    class Media:
        js = ("js/admin_row_click.js",)


@admin.register(TicketStatus)
class TicketStatusAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    class Media:
        js = ("js/admin_row_click.js",)
