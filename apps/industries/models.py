from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel


class Industry(BaseModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    services_offered = models.TextField(
        blank=True,
        default="",
        help_text="One relevant service/benefit per line shown on detail page.",
    )
    image = models.CharField(
        max_length=80,
        blank=True,
        default="",
        help_text="Filename from static/images/industry/ e.g. 01.webp",
    )
    featured_product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="featured_in_industries",
        help_text="Optional BJP product recommended on this industry's page.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_services_list(self) -> list[str]:
        return [line.strip() for line in self.services_offered.splitlines() if line.strip()]
