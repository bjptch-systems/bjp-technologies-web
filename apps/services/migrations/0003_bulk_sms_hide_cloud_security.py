from django.db import migrations

# Paused (Nov 2026) — hidden, not deleted, so admin can switch them back on.
HIDDEN_SLUGS = ["cloud-infrastructure", "cybersecurity"]

BULK_SMS = {
    "name": "Bulk SMS",
    "slug": "bulk-sms",
    "tagline": "Reach thousands of customers with one message",
    "order": 7,
    "icon_svg": "",
    "image": "bjp-bulk-sms.webp",
    "description": (
        "Bulk SMS lets you send alerts, reminders, promotions and updates to many people at "
        "once, straight to their phones. Messages go out under your own business name as the "
        "sender ID, so customers know who is writing. Run campaigns to your whole customer or "
        "member list, or connect your own system through our SMS API to send messages "
        "automatically, such as payment reminders, receipts and appointment confirmations."
    ),
    "bullet_points": (
        "Custom Sender ID — messages show your business name\n"
        "Bulk Campaigns — reach whole customer or member lists at once\n"
        "SMS API — send automatically from your own system or app\n"
        "Alerts, reminders, confirmations and promotions"
    ),
}

CONSULTING_OLD_DESCRIPTION = (
    "Technology decisions made today shape your business for years. Our consulting "
    "team works alongside your leadership to design infrastructure that scales, plan "
    "cloud migrations that reduce cost, and build cybersecurity postures that satisfy "
    "compliance requirements. We translate technical complexity into clear business "
    "decisions — so you invest in the right things."
)
CONSULTING_NEW_DESCRIPTION = (
    "Technology decisions made today shape your business for years. Our consulting "
    "team works alongside your leadership to plan systems that scale, choose the right "
    "technology for each job, and guide your digital transformation step by step. We "
    "translate technical complexity into clear business decisions — so you invest in the "
    "right things."
)
CONSULTING_OLD_BULLETS = (
    "IT Infrastructure Design & Planning\n"
    "Cloud Migration & Optimisation\n"
    "Cybersecurity & Compliance Advisory\n"
    "Digital Transformation Strategy"
)
CONSULTING_NEW_BULLETS = (
    "IT Systems Design & Planning\n"
    "Digital Transformation Strategy\n"
    "Technology Roadmap Planning"
)


def forwards(apps, schema_editor):
    """Hide Cloud & Infrastructure and Cybersecurity, add Bulk SMS, and drop cloud and
    security wording from IT Consulting. Text is only replaced while it still matches
    the original seeded wording — admin edits are never overwritten."""
    Service = apps.get_model("services", "Service")
    Service.objects.filter(slug__in=HIDDEN_SLUGS).update(is_active=False)

    defaults = {k: v for k, v in BULK_SMS.items() if k != "slug"}
    Service.objects.get_or_create(slug=BULK_SMS["slug"], defaults=defaults)

    Service.objects.filter(
        slug="it-consulting-advisory", description=CONSULTING_OLD_DESCRIPTION
    ).update(description=CONSULTING_NEW_DESCRIPTION)
    Service.objects.filter(
        slug="it-consulting-advisory", bullet_points=CONSULTING_OLD_BULLETS
    ).update(bullet_points=CONSULTING_NEW_BULLETS)


def backwards(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.filter(slug__in=HIDDEN_SLUGS).update(is_active=True)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0002_service_image"),
    ]
    operations = [migrations.RunPython(forwards, backwards)]
