from django.db import migrations, models

SERVICE_SLUGS = [
    "software-development",
    "website-digital-solutions",
    "cloud-infrastructure",
    "cybersecurity",
    "managed-it-services",
    "payment-system-integrations",
    "it-consulting-advisory",
]


def set_images(apps, schema_editor):
    """Give each seeded service its branded image. Only fills blanks — never
    overrides an image an admin has since set."""
    Service = apps.get_model("services", "Service")
    for slug in SERVICE_SLUGS:
        Service.objects.filter(slug=slug, image="").update(image=f"bjp-{slug}.webp")


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="service",
            name="image",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Filename from static/images/service/ e.g. bjp-cybersecurity.webp",
                max_length=80,
            ),
        ),
        migrations.RunPython(set_images, migrations.RunPython.noop),
    ]
