from django.urls import reverse_lazy

# from django.urls import reverse, reverse_lazy


def can_manage_users(request):
    return request.user.is_superuser or request.user.has_perm("auth.view_user")


def can_manage_groups(request):
    return request.user.is_superuser or request.user.has_perm("auth.view_group")


UNFOLD = {
    "DASHBOARD_CALLBACK": "dashboard.views.dashboard_callback",
    "SITE_TITLE": "Internal Application - The Deep Seafood",
    "SITE_HEADER": "Internal Application",
    "SITE_SUBHEADER": "The Deep Seafood",
    "SHOW_BACK_BUTTON": True,
    "THEME": "dark",
    "SIDEBAR": {
        "show_search": True,
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
                "title": ("Tasks Management"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Projects",
                        "icon": "analytics",
                        "link": reverse_lazy("admin:tasks_dashboard"),
                    },
                    {
                        "title": "Daily Tasks",
                        "icon": "calendar_today",
                        "link": reverse_lazy("admin:daily_task_dashboard"),
                    },
                    {
                        "title": "Brands",
                        "icon": "label",
                        "link": reverse_lazy("admin:tasks_brand_changelist"),
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
            {
                "title": "User Management",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": can_manage_users,
                    },
                    {
                        "title": "Groups & Permissions",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": can_manage_groups,
                    },
                ],
            },
        ],
    },
}
