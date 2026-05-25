from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

# from django.utils.html import format_html
from unfold.admin import ModelAdmin

from credentials.models import Credential


@admin.register(Credential)
class CredentialAdmin(ModelAdmin):
    list_display = (
        "name",
        "user_id",
        "email",
        "password",
        "notes",
        "copy_credential",
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

    @admin.display(description="Copy")
    def copy_credential(self, obj):
        copy_text = f"""Name: {obj.name or ""}\nUser ID: {obj.user_id or ""}\nEmail: {obj.email or ""}\nPassword: {obj.password or ""}\nURL: {obj.url or ""}"""

        html = render_to_string(
            "credentials/copy_credential_button.html",
            {
                "copy_text": copy_text,
            },
        )

        return mark_safe(html)

    class Media:
        js = (
            # "js/admin_row_click.js",
            "credentials/js/credential_copy.js",
        )
