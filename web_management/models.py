from django.db import models
from django.utils import timezone


class Registrar(models.Model):
    name = models.CharField(max_length=150, unique=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class DomainManager(models.Model):
    domain_name = models.CharField(max_length=255, unique=True)
    registrar = models.ForeignKey(
        Registrar, on_delete=models.SET_NULL, null=True, blank=True
    )
    expiry_date = models.DateField()
    renewal_status = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def days_until_expiry(self):
        return (self.expiry_date - timezone.now().date()).days

    def __str__(self):
        return self.domain_name


class WebPageManager(models.Model):
    domain = models.ForeignKey(
        DomainManager, on_delete=models.CASCADE, related_name="webpages"
    )
    page_title = models.CharField(max_length=255)
    page_url = models.URLField()
    purpose = models.TextField(blank=True, null=True)
    managed_by = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page_title


class WebFormManager(models.Model):
    webpage = models.ForeignKey(
        WebPageManager, on_delete=models.CASCADE, related_name="forms"
    )
    form_name = models.CharField(max_length=255)
    form_url = models.URLField(blank=True, null=True)
    form_purpose = models.TextField()
    submission_receiver = models.EmailField(blank=True, null=True)
    stores_data = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.form_name
