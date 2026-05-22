from django import forms
from unfold.widgets import UnfoldAdminTextareaWidget

from web_management.models import DNSZone


class DNSZoneAdminForm(forms.ModelForm):
    class Meta:
        model = DNSZone
        fields = "__all__"

        widgets = {
            "dns_records": UnfoldAdminTextareaWidget(
                attrs={
                    "rows": 30,
                    "class": "font-mono whitespace-pre",
                }
            )
        }
