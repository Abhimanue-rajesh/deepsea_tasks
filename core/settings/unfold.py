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
                "title": ("Overview"),
                "collapsible": False,
                "items": [
                    {
                        "title": ("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": ("Task Management"),
                "collapsible": False,
                "separator": True,
                "items": [
                    {
                        "title": ("Tasks"),
                        "icon": "task",
                        "link": reverse_lazy("admin:tasks_task_changelist"),
                    },
                ],
            },
            {
                "title": ("Ticketing"),
                "collapsible": False,
                "separator": True,
                "items": [
                    {
                        "title": ("Support Tickets"),
                        "icon": "confirmation_number",
                        "link": reverse_lazy("admin:tickets_supportticket_changelist"),
                    },
                    {
                        "title": ("Ticket Routing"),
                        "icon": "route",
                        "link": reverse_lazy("admin:tickets_ticketrouting_changelist"),
                    },
                    {
                        "title": ("Ticket Status"),
                        "icon": "flag",
                        "link": reverse_lazy("admin:tickets_ticketstatus_changelist"),
                    },
                ],
            },
            {
                "title": ("Credentials"),
                "collapsible": False,
                "separator": True,
                "items": [
                    {
                        "title": ("Credentials"),
                        "icon": "key",
                        "link": reverse_lazy("admin:credentials_credential_changelist"),
                    },
                ],
            },
            {
                "title": ("Web Management"),
                "collapsible": False,
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
                    # {
                    #     "title": ("Web Forms"),
                    #     "icon": "description",
                    #     "link": reverse_lazy(
                    #         "admin:web_management_webformmanager_changelist"
                    #     ),
                    # },
                    {
                        "title": ("DNS Zones"),
                        "icon": "article",
                        "link": reverse_lazy("admin:web_management_dnszone_changelist"),
                    },
                ],
            },
            # {
            #     "title": ("Account"),
            #     "collapsible": False,
            #     "separator": True,
            #     "items": [
            #         {
            #             "title": ("My Profile"),
            #             "icon": "person",
            #             "link": lambda request: reverse(
            #                 "admin:auth_user_change",
            #                 args=[request.user.id],
            #             ),
            #         },
            #     ],
            # },
        ],
    },
}
