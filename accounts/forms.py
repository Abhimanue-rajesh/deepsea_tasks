from collections import defaultdict

from django import forms
from django.contrib.auth.models import Group, Permission


class GroupPermissionForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_ids = set()

        if self.instance and self.instance.pk:
            selected_ids = set(self.instance.permissions.values_list("id", flat=True))

        permissions = Permission.objects.select_related("content_type").order_by(
            "content_type__app_label",
            "content_type__model",
            "codename",
        )

        grouped = defaultdict(
            lambda: defaultdict(
                lambda: {
                    "view": [],
                    "add": [],
                    "change": [],
                    "delete": [],
                    "other": [],
                }
            )
        )

        for permission in permissions:
            app_label = permission.content_type.app_label
            model_name = permission.content_type.model

            action = self.get_action(permission.codename)

            grouped[app_label][model_name][action].append(
                {
                    "id": permission.pk,
                    "name": permission.name,
                    "codename": permission.codename,
                    "selected": permission.pk in selected_ids,
                }
            )

        # Convert nested dictionaries into template-friendly lists
        self.permission_groups = []

        for app_label, models in grouped.items():
            app_data = {
                "app_label": app_label,
                "app_name": app_label.replace("_", " ").title(),
                "models": [],
            }

            for model_name, actions in models.items():
                app_data["models"].append(
                    {
                        "model_name": model_name,
                        "display_name": model_name.replace("_", " ").title(),
                        "view": actions["view"],
                        "add": actions["add"],
                        "change": actions["change"],
                        "delete": actions["delete"],
                        "other": actions["other"],
                    }
                )

            self.permission_groups.append(app_data)

    @staticmethod
    def get_action(codename):
        if codename.startswith("view_"):
            return "view"

        if codename.startswith("add_"):
            return "add"

        if codename.startswith("change_"):
            return "change"

        if codename.startswith("delete_"):
            return "delete"

        return "other"

    def save_permissions(self, group):
        permission_ids = self.data.getlist("permissions")
        group.permissions.set(permission_ids)
