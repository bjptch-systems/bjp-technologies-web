import uuid

from django.db import models

from .validators import validate_favicon_file, validate_logo_file


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Singleton — only one row ever exists. Edit via admin, never create a second."""

    name = models.CharField(max_length=120, default="BJP Technologies (T) Limited")
    tagline = models.CharField(max_length=200, default="Secure Technology. Scalable Growth.")
    email = models.EmailField(default="info@bjptechnologies.co.tz")
    phone = models.CharField(max_length=30, default="+255 678 290 994")
    address = models.CharField(max_length=200, default="Ubungo – Dar es Salaam, Tanzania")
    postal = models.CharField(max_length=100, default="P.O Box 7276, Msakuzi – Mbezi")
    domain = models.CharField(max_length=100, default="bjptechnologies.co.tz")

    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")

    # Home page — Hero
    hero_headline = models.CharField(max_length=200, default="Secure Technology. Scalable Growth.")
    hero_subtext = models.TextField(
        default=(
            "Tanzania's trusted IT partner — delivering tailored software, cybersecurity, "
            "cloud, and payment integration solutions that drive real business growth."
        )
    )
    hero_cta_primary = models.CharField(max_length=60, default="Get Free Consultation")
    hero_cta_secondary = models.CharField(max_length=60, default="Our Services")

    # Home page — Stats counters
    stat_1_value = models.CharField(max_length=20, default="7")
    stat_1_label = models.CharField(max_length=60, default="IT Service Lines")
    stat_2_value = models.CharField(max_length=20, default="6")
    stat_2_label = models.CharField(max_length=60, default="Industries Served")
    stat_3_value = models.CharField(max_length=20, default="24/7")
    stat_3_label = models.CharField(max_length=60, default="Monitoring & Support")
    stat_4_value = models.CharField(max_length=20, default="100%")
    stat_4_label = models.CharField(max_length=60, default="Dedicated to Your Success")

    # Home page — About strip
    about_headline = models.CharField(
        max_length=200, default="Tanzania's IT Partner Built for East Africa"
    )
    about_body = models.TextField(
        default=(
            "BJP Technologies (T) Limited is a full-service IT company headquartered in "
            "Ubungo, Dar es Salaam. We build and maintain the software, infrastructure, "
            "and security systems that keep growing businesses running — from Tanzanian "
            "startups to regional enterprises."
        )
    )

    # About page — banner + counters + body
    about_banner_headline = models.CharField(
        max_length=200, default="Secure Technology. Scalable Growth."
    )
    about_stat_1_value = models.CharField(max_length=20, default="50+")
    about_stat_1_label = models.CharField(max_length=60, default="Projects Delivered")
    about_stat_2_value = models.CharField(max_length=20, default="30+")
    about_stat_2_label = models.CharField(max_length=60, default="Happy Clients")
    about_stat_3_value = models.CharField(max_length=20, default="20+")
    about_stat_3_label = models.CharField(max_length=60, default="Security Audits Done")
    about_stat_4_value = models.CharField(max_length=20, default="5+")
    about_stat_4_label = models.CharField(max_length=60, default="Years in Business")
    about_intro = models.TextField(
        default=(
            "BJP Technologies (T) Limited is a Tanzanian IT solutions company headquartered "
            "in Ubungo, Dar es Salaam. We deliver enterprise-grade technology services — from "
            "custom software development and cloud infrastructure to cybersecurity and managed "
            "IT — helping businesses across East Africa grow securely and operate at scale."
        )
    )
    about_what_we_do = models.TextField(
        default=(
            "We bring together the technology, expertise, and support businesses need to solve "
            "real problems. From secure web applications to cloud infrastructure and mobile money "
            "payment integrations — we cover the full technology stack so our clients can focus "
            "on growth."
        )
    )
    about_our_approach = models.TextField(
        default=(
            "We believe every client deserves solutions tailored to their context — not generic "
            "off-the-shelf products. Our team works closely with each organisation to understand "
            "their operations, constraints, and goals before recommending or building anything."
        )
    )

    # Services page — banner
    services_banner_headline = models.CharField(
        max_length=200, default="Enterprise IT Solutions Built for Tanzania"
    )
    services_banner_subtext = models.TextField(
        default=(
            "From custom software to cloud infrastructure — we deliver secure, scalable "
            "technology that helps businesses across East Africa grow with confidence."
        )
    )

    # Industries page — banner
    industries_banner_headline = models.CharField(
        max_length=200, default="Tailored Solutions for Every Industry"
    )
    industries_banner_subtext = models.TextField(
        default=(
            "We understand that different sectors have unique technology needs. "
            "BJP Technologies delivers solutions built around your industry's specific challenges."
        )
    )

    # Contact page
    maps_embed_url = models.CharField(
        max_length=500,
        default="https://www.google.com/maps?q=-6.750417,39.090111&z=17&output=embed",
    )

    # Branding — logo & favicon
    logo = models.FileField(
        upload_to="branding/",
        blank=True,
        validators=[validate_logo_file],
        help_text=(
            "Accepted: SVG, PNG, WebP. Must have a transparent background. "
            "Used in the navbar and footer on dark navy backgrounds."
        ),
    )
    favicon = models.FileField(
        upload_to="branding/",
        blank=True,
        validators=[validate_favicon_file],
        help_text="Accepted: PNG, ICO. Must be square — 32×32 pixels minimum, 64×64 recommended.",
    )

    # Footer CTA
    footer_cta_headline = models.CharField(
        max_length=200, default="Ready to Transform Your Business?"
    )
    footer_cta_body = models.TextField(
        default=(
            "Schedule a free consultation with our team. We'll assess your needs "
            "and recommend the right technology solutions for your organisation."
        )
    )
    footer_cta_button = models.CharField(max_length=60, default="Get Free Consultation")

    # Google Analytics (GA4)
    ga_measurement_id = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text="GA4 Measurement ID (starts with G-). Leave blank to disable tracking.",
    )
    ga_enabled = models.BooleanField(
        default=True,
        help_text=(
            "Master switch — uncheck to disable analytics site-wide without removing the ID. "
            "Tracking is also suppressed automatically when DEBUG is on (local development)."
        ),
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self) -> str:
        return "Site Settings"

    def save(self, *args, **kwargs) -> None:
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class CompanyIdentitySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Company Identity"
        verbose_name_plural = "Company Identity"


class AddressSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Address"
        verbose_name_plural = "Address"


class SocialMediaSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Social Media Links"
        verbose_name_plural = "Social Media Links"


class HeroSectionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"


class StatsCountersSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Stats Counters"
        verbose_name_plural = "Stats Counters"


class AboutStripSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "About Strip"
        verbose_name_plural = "About Strip"


class AboutPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "About Page"
        verbose_name_plural = "About Page"


class ServicesPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Services Page"
        verbose_name_plural = "Services Page"


class IndustriesPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Industries Page"
        verbose_name_plural = "Industries Page"


class ContactPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Page"


class FooterCTASettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Footer CTA"
        verbose_name_plural = "Footer CTA"


class LogoBrandingSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Logo & Branding"
        verbose_name_plural = "Logo & Branding"


class AnalyticsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Google Analytics"
        verbose_name_plural = "Google Analytics"
