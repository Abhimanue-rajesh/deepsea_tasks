from django.urls import reverse_lazy


def group_permission(*group_names):
    """
    Allow access to superusers or users belonging to any supplied group.
    """

    def check(request):
        user = request.user

        return user.is_authenticated and (
            user.is_superuser or user.groups.filter(name__in=group_names).exists()
        )

    return check


def can_manage_users(request):
    user = request.user

    return user.is_authenticated and (
        user.is_superuser or user.has_perm("auth.view_user")
    )


def can_manage_groups(request):
    user = request.user

    return user.is_authenticated and (
        user.is_superuser or user.has_perm("auth.view_group")
    )


can_view_support_tickets = group_permission(
    "Support Ticket Users",
    "Support Ticket Managers",
)

can_view_credentials = group_permission(
    "Credential Managers",
)

can_view_tasks = group_permission(
    "Task Users",
    "Task Managers",
)

can_view_daily_tasks = group_permission(
    "Daily Task Users",
    "Daily Task Managers",
)

can_view_web_management = group_permission(
    "Web Management",
)

can_view_subscriptions = group_permission(
    "Subscription Managers",
)


# ---------------------------------------------------------------------
# Unfold configuration
# ---------------------------------------------------------------------

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
                "title": "Navigation",
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Support Tickets",
                        "icon": "confirmation_number",
                        "link": reverse_lazy("admin:tickets_supportticket_changelist"),
                        "permission": can_view_support_tickets,
                    },
                    {
                        "title": "Credentials",
                        "icon": "key",
                        "link": reverse_lazy("admin:credentials_credential_changelist"),
                        "permission": can_view_credentials,
                    },
                    {
                        "title": "Subscriptions",
                        "icon": "subscriptions",
                        "link": reverse_lazy(
                            "admin:subscriptions_subscriptiontracker_changelist"
                        ),
                        "permission": can_view_subscriptions,
                    },
                ],
            },
            {
                "title": "Tasks Management",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Projects",
                        "icon": "analytics",
                        "link": reverse_lazy("admin:tasks_dashboard"),
                        "permission": can_view_tasks,
                    },
                    {
                        "title": "Daily Tasks",
                        "icon": "calendar_today",
                        "link": reverse_lazy("admin:daily_task_dashboard"),
                        "permission": can_view_daily_tasks,
                    },
                    {
                        "title": "Brands",
                        "icon": "label",
                        "link": reverse_lazy("admin:tasks_brand_changelist"),
                        "permission": can_view_tasks,
                    },
                ],
            },
            {
                "title": "Web Management",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Domains",
                        "icon": "language",
                        "link": reverse_lazy(
                            "admin:web_management_domainmanager_changelist"
                        ),
                        "permission": can_view_web_management,
                    },
                    {
                        "title": "Domain Registrars",
                        "icon": "dns",
                        "link": reverse_lazy(
                            "admin:web_management_registrar_changelist"
                        ),
                        "permission": can_view_web_management,
                    },
                    {
                        "title": "Web Pages and Forms",
                        "icon": "web",
                        "link": reverse_lazy(
                            "admin:web_management_webpagemanager_changelist"
                        ),
                        "permission": can_view_web_management,
                    },
                    {
                        "title": "DNS Zones",
                        "icon": "article",
                        "link": reverse_lazy("admin:web_management_dnszone_changelist"),
                        "permission": can_view_web_management,
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
