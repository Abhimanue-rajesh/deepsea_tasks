from django.urls import reverse_lazy

# from django.urls import reverse, reverse_lazy

UNFOLD = {
    "DASHBOARD_CALLBACK": "dashboard.views.dashboard_callback",
    "SITE_TITLE": "Task Management",
    "SITE_HEADER": "Task Management Admin",
    "SITE_SUBHEADER": "Administration",
    "SHOW_BACK_BUTTON": True,
    "THEME": "dark",
    "SIDEBAR": {
        "show_search": False,
        "navigation": [
            {
                "title": ("Navigation"),
                "items": [
                    {
                        "title": ("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": ("Tasks"),
                        "icon": "task",
                        "link": reverse_lazy("admin:tasks_task_changelist"),
                    },
                    {
                        "title": ("Support Tickets"),
                        "icon": "confirmation_number",
                        "link": reverse_lazy("admin:tickets_supportticket_changelist"),
                    },
                    {
                        "title": ("Credentials"),
                        "icon": "key",
                        "link": reverse_lazy("admin:credentials_credential_changelist"),
                    },
                    {
                        "title": ("Quick Copy Items"),
                        "icon": "content_copy",
                        "link": reverse_lazy("admin:quickcopy_quickcopy_changelist"),
                    },
                    {
                        "title": ("Subscriptions"),
                        "icon": "subscriptions",
                        "link": reverse_lazy(
                            "admin:subscriptions_subscriptiontracker_changelist"
                        ),
                    },
                ],
            },
            {
                "title": ("Web Management"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": ("Domains"),
                        "icon": "language",
                        "link": reverse_lazy(
                            "admin:web_management_domainmanager_changelist"
                        ),
                    },
                    {
                        "title": ("Domain Registrars"),
                        "icon": "dns",
                        "link": reverse_lazy(
                            "admin:web_management_registrar_changelist"
                        ),
                    },
                    {
                        "title": ("Web Pages and Forms"),
                        "icon": "web",
                        "link": reverse_lazy(
                            "admin:web_management_webpagemanager_changelist"
                        ),
                    },
                    {
                        "title": ("DNS Zones"),
                        "icon": "article",
                        "link": reverse_lazy("admin:web_management_dnszone_changelist"),
                    },
                ],
            },
        ],
    },
}
