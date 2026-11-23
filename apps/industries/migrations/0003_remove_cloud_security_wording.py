from django.db import migrations

# slug -> list of (old, new). Each pair is applied only where the old text is still
# present, so wording an admin has since changed is left alone.
SERVICE_LINES = {
    "startups-smes": [
        (
            "Cloud infrastructure setup on DigitalOcean or AWS",
            "Bulk SMS for customer alerts and promotions",
        ),
    ],
    "financial-institutions": [
        (
            "Cybersecurity hardening and VAPT assessments",
            "Bulk SMS alerts for members and customers",
        ),
    ],
    "ngos-development": [
        (
            "Cloud infrastructure setup and management",
            "Bulk SMS for beneficiary and community updates",
        ),
    ],
    "education": [
        ("Cloud-based data storage and backup", "Data storage and backup"),
        (
            "Network infrastructure setup and management",
            "Bulk SMS for parents, students and staff",
        ),
        (
            "Cybersecurity awareness and endpoint protection",
            "School fees payment integrations (mobile money)",
        ),
    ],
    "healthcare": [
        (
            "Cybersecurity hardening and access control",
            "Access control so staff see only what they need",
        ),
        ("24/7 infrastructure monitoring", "24/7 system monitoring"),
        (
            "Cloud migration for healthcare applications",
            "Bulk SMS appointment reminders",
        ),
    ],
    "retail-wholesale": [
        (
            "Cloud infrastructure for multi-branch operations",
            "Bulk SMS for promotions and customer updates",
        ),
    ],
}

DESCRIPTION_PHRASES = {
    "financial-institutions": [("and secure infrastructure that", "and reliable systems that")],
    "ngos-development": [
        (
            "websites, data systems, and cloud infrastructure that keep",
            "websites, data systems, and SMS communication that keep",
        ),
    ],
    "education": [
        ("and the secure infrastructure that keeps", "and the reliable systems that keep")
    ],
    "healthcare": [("the systems, secure infrastructure, and", "the systems and")],
}


def forwards(apps, schema_editor):
    """Replace cloud and cybersecurity mentions now those services are paused."""
    Industry = apps.get_model("industries", "Industry")
    for industry in Industry.objects.filter(slug__in=set(SERVICE_LINES) | set(DESCRIPTION_PHRASES)):
        changed = []
        lines = industry.services_offered.split("\n")
        for old, new in SERVICE_LINES.get(industry.slug, []):
            lines = [new if line.strip() == old else line for line in lines]
        services_offered = "\n".join(lines)
        if services_offered != industry.services_offered:
            industry.services_offered = services_offered
            changed.append("services_offered")
        description = industry.description
        for old, new in DESCRIPTION_PHRASES.get(industry.slug, []):
            description = description.replace(old, new)
        if description != industry.description:
            industry.description = description
            changed.append("description")
        if changed:
            industry.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("industries", "0002_branded_industry_images"),
    ]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
