from django.db import migrations, models

# slug -> (template SVG it was seeded with, Font Awesome class). The old SVG names were
# rendered as CSS classes, so the services list showed empty icon boxes.
ICONS = {
    "software-development": ("22.svg", "fa-regular fa-laptop-code"),
    "website-digital-solutions": ("23.svg", "fa-regular fa-globe"),
    "cloud-infrastructure": ("24.svg", "fa-regular fa-cloud-arrow-up"),
    "cybersecurity": ("25.svg", "fa-regular fa-shield-halved"),
    "managed-it-services": ("26.svg", "fa-regular fa-headset"),
    "payment-system-integrations": ("27.svg", "fa-regular fa-mobile-screen-button"),
    "it-consulting-advisory": ("28.svg", "fa-regular fa-lightbulb"),
    "bulk-sms": ("", "fa-regular fa-comment-sms"),
}


def forwards(apps, schema_editor):
    """Give every service a working icon and put IT Consulting after Bulk SMS (both
    had order 7). Only touches values still at their seeded defaults."""
    Service = apps.get_model("services", "Service")
    for slug, (old, new) in ICONS.items():
        Service.objects.filter(slug=slug, icon_svg=old).update(icon_svg=new)
    Service.objects.filter(slug="it-consulting-advisory", order=7).update(order=8)


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0003_bulk_sms_hide_cloud_security"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="icon_svg",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Font Awesome icon class, e.g. fa-regular fa-laptop-code",
                max_length=60,
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
