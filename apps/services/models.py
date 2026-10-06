from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel


class Service(BaseModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    bullet_points = models.TextField(
        blank=True,
        default="",
        help_text="One bullet point per line.",
    )
    icon_svg = models.CharField(
        max_length=60,
        blank=True,
        default="",
        help_text="Filename from static/images/service/icons/ e.g. 22.svg",
    )
    image = models.CharField(
        max_length=80,
        blank=True,
        default="",
        help_text="Filename from static/images/service/ e.g. bjp-cybersecurity.webp",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_bullet_list(self) -> list[str]:
        return [line.strip() for line in self.bullet_points.splitlines() if line.strip()]
