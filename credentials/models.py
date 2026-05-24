from django.core.exceptions import ValidationError
from django.db import models

from credentials.fields import EncryptedTextField


def validate_pem_file(value):
    if not value.name.endswith(".pem"):
        raise ValidationError("Only .pem files are allowed.")


class Credential(models.Model):
    name = models.CharField(
        max_length=255,
    )
    user_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )
    password = EncryptedTextField(
        max_length=500,
        blank=True,
        null=True,
    )
    url = models.URLField(
        blank=True,
        null=True,
    )
    pem_file = models.FileField(
        upload_to="credentials/pem_files/",
        validators=[validate_pem_file],
        blank=True,
        null=True,
    )
    notes = EncryptedTextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Credential"
        verbose_name_plural = "Credentials"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        pem_file = self.pem_file
        super().delete(*args, **kwargs)

        if pem_file:
            pem_file.delete(save=False)

    def clean(self):
        super().clean()

        if not self.password and not self.pem_file:
            raise ValidationError(
                {
                    "password": "Either password or PEM file is required.",
                    "pem_file": "Either password or PEM file is required.",
                }
            )
