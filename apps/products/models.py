from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel


class Product(BaseModel):
    STATUS_LIVE = "live"
    STATUS_COMING_SOON = "coming-soon"
    STATUS_CHOICES = [
        (STATUS_LIVE, "Live"),
        (STATUS_COMING_SOON, "Coming Soon"),
    ]

    # Identity
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True, default="")
    byline = models.CharField(max_length=300, blank=True, default="")
    live_url = models.URLField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_LIVE,
        help_text="Only 'Live' products appear on the public site.",
    )

    # Descriptions
    short_description = models.TextField(
        blank=True,
        default="",
        help_text="Used on the home-page card and products list. Aim for ≤60 words.",
    )
    long_description = models.TextField(
        blank=True,
        default="",
        help_text="2-3 paragraphs. Used in the detail page hero. Plain text — line breaks become paragraphs.",
    )

    # Detail page sections
    problem_statements = models.TextField(
        blank=True,
        default="",
        help_text="One bullet per line. Rendered as the 'What it solves' list.",
    )
    target_users = models.TextField(
        blank=True,
        default="",
        help_text="One user type per line. Format: 'Type — what they use it for.'",
    )
    features = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            'List of feature dicts: [{"name": "...", "description": "...", '
            '"icon": "bi-buildings"}]. Icon is a Bootstrap Icons class name.'
        ),
    )
    differentiators = models.TextField(
        blank=True,
        default="",
        help_text="One per line. Rendered as the 'What makes it different' list.",
    )
    how_it_works_steps = models.TextField(
        blank=True,
        default="",
        help_text="One step per line. Rendered as a numbered process.",
    )
    pricing_summary = models.TextField(
        blank=True,
        default="",
        help_text="1-2 sentences describing how pricing works.",
    )
    onboarding_promise = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Single line — e.g. 'Get started in 24 hours.'",
    )

    # CTAs
    cta_primary_label = models.CharField(max_length=60, blank=True, default="Request a demo")
    cta_primary_url = models.URLField(
        blank=True,
        default="",
        help_text="Where the primary CTA points. Usually the live product URL.",
    )
    cta_secondary_label = models.CharField(max_length=60, blank=True, default="Take the tour")
    cta_secondary_url = models.URLField(blank=True, default="")

    # Conditional contact block (rendered only when at least one field is populated)
    contact_email = models.EmailField(blank=True, default="")
    contact_phone = models.CharField(max_length=30, blank=True, default="")
    contact_hours = models.CharField(max_length=150, blank=True, default="")
    contact_whatsapp = models.CharField(max_length=30, blank=True, default="")

    # SEO
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        default="",
        help_text="≤60 characters recommended. Falls back to product name if empty.",
    )
    meta_description = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="≤155 characters recommended. Falls back to short description if empty.",
    )

    # Assets — relative paths under static/images/
    hero_image = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text=(
            "Relative path under static/images/, e.g. 'products/pms/hero-dashboard.png'. "
            "Copy the file into the corresponding static/images/ folder."
        ),
    )
    og_image = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Open Graph share card. Relative path under static/images/.",
    )
    logo_image = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Optional product logo (SVG or PNG). Relative path under static/images/.",
    )
    accent_color = models.CharField(
        max_length=7,
        blank=True,
        default="",
        help_text="Optional hex color (e.g. #0F766E) for a subtle product badge.",
    )
    screenshots = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            'List of screenshot dicts: [{"image": "products/pms/feature-x.png", '
            '"caption": "What this shows"}].'
        ),
    )

    # Display
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_live(self) -> bool:
        return self.status == self.STATUS_LIVE

    @property
    def has_contact_block(self) -> bool:
        return any(
            [self.contact_email, self.contact_phone, self.contact_hours, self.contact_whatsapp]
        )

    def get_problem_list(self) -> list[str]:
        return [line.strip() for line in self.problem_statements.splitlines() if line.strip()]

    def get_target_users_list(self) -> list[str]:
        return [line.strip() for line in self.target_users.splitlines() if line.strip()]

    def get_differentiators_list(self) -> list[str]:
        return [line.strip() for line in self.differentiators.splitlines() if line.strip()]

    def get_how_it_works_list(self) -> list[str]:
        return [line.strip() for line in self.how_it_works_steps.splitlines() if line.strip()]
