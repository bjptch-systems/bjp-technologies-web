from django.db import migrations

# slug -> template image it was seeded with
OLD_IMAGES = {
    "startups-smes": "01.webp",
    "financial-institutions": "02.webp",
    "ngos-development": "03.webp",
    "education": "06.webp",
    "healthcare": "07.webp",
    "retail-wholesale": "08.webp",
}


def set_images(apps, schema_editor):
    """Swap each seeded industry from its template image to its branded one.
    Only replaces the original seeded value or a blank — never overrides an
    image an admin has since chosen."""
    Industry = apps.get_model("industries", "Industry")
    for slug, old in OLD_IMAGES.items():
        Industry.objects.filter(slug=slug, image__in=[old, ""]).update(image=f"bjp-{slug}.webp")


class Migration(migrations.Migration):
    dependencies = [
        ("industries", "0001_initial"),
    ]
    operations = [migrations.RunPython(set_images, migrations.RunPython.noop)]
