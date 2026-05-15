from django.urls import reverse, reverse_lazy

UNFOLD = {
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
                "title": ("Account"),
                "collapsible": False,
                "separator": True,
                "items": [
                    {
                        "title": ("My Profile"),
                        "icon": "person",
                        "link": lambda request: reverse(
                            "admin:auth_user_change",
                            args=[request.user.id],
                        ),
                    },
                ],
            },
        ],
    },
}
