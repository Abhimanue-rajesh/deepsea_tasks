from django.contrib import admin
from unfold.admin import ModelAdmin

from credentials.models import Credential


@admin.register(Credential)
class CredentialAdmin(ModelAdmin):
    list_display = (
        "name",
        "user_id",
        "email",
        "url",
        "has_pem_file",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "user_id",
        "email",
        "url",
        "notes",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Credential Details",
            {
                "fields": (
                    "name",
                    "user_id",
                    "email",
                    "password",
                    "url",
                    "pem_file",
                    "notes",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="PEM File")
    def has_pem_file(self, obj):
        return "Yes" if obj.pem_file else "No"
