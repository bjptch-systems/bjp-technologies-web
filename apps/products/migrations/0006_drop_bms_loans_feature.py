"""Remove the "Loans / Microfinance" feature from the BMS product record.

The BMS team brief listed Loans/Microfinance as a module, but it isn't
actually integrated in the shipped BMS build today — per user direction
it must come off the public page. Vikundi's own Loans & repayments
feature is a separate module and stays.

Idempotent (only removes the entry if present); reverse re-adds it with
the original copy and icon from migration 0005.
"""

from django.db import migrations

LOANS_FEATURE_NAME = "Loans / Microfinance"

LOANS_FEATURE_PAYLOAD = {
    "name": LOANS_FEATURE_NAME,
    "description": (
        "Issue loans, schedule repayments and monitor overdue balances and " "portfolio risk."
    ),
    "icon": "fa-regular fa-coins",
}


def remove_loans(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    bms = Product.objects.filter(slug="bms").first()
    if not bms:
        return
    features = bms.features or []
    new_features = [f for f in features if f.get("name") != LOANS_FEATURE_NAME]
    if len(new_features) != len(features):
        bms.features = new_features
        bms.save(update_fields=["features"])


def restore_loans(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    bms = Product.objects.filter(slug="bms").first()
    if not bms:
        return
    features = bms.features or []
    if any(f.get("name") == LOANS_FEATURE_NAME for f in features):
        return
    features.append(LOANS_FEATURE_PAYLOAD)
    bms.features = features
    bms.save(update_fields=["features"])


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_seed_bms_vikundi"),
    ]

    operations = [
        migrations.RunPython(remove_loans, restore_loans),
    ]
