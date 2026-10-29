from django.db import models

from apps.core.models import BaseModel
from apps.services.models import Service


class ContactEnquiry(BaseModel):
    STATUS_NEW = "new"
    STATUS_READ = "read"
    STATUS_REPLIED = "replied"
    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_READ, "Read"),
        (STATUS_REPLIED, "Replied"),
    ]

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, default="")
    company = models.CharField(max_length=120, blank=True, default="")
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enquiries",
    )
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_NEW)
    consent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the visitor ticked the privacy consent box. Blank for older enquiries.",
    )
    privacy_policy_version = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text="'Last updated' date of the Privacy Policy the visitor agreed to.",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Enquiry"
        verbose_name_plural = "Contact Enquiries"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} — {self.email}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
