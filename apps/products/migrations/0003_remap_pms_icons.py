"""Remap PMS feature icons from Bootstrap Icons to Font Awesome.

Original seed (0002) used Bootstrap Icons (bi-*), loaded via a public CDN.
The live site CSP blocks that CDN, so the glyphs never render. Font Awesome
Pro is already loaded site-wide via static/css/plugins/fontawesome.css and
is the convention for every other icon on the site — switch PMS to match.

Idempotent: only updates entries that still have the bi-* values.
"""

from django.db import migrations

BI_TO_FA = {
    "bi-buildings": "fa-regular fa-buildings",
    "bi-file-earmark-text": "fa-regular fa-file-lines",
    "bi-receipt": "fa-regular fa-receipt",
    "bi-cash-coin": "fa-regular fa-coins",
    "bi-tools": "fa-regular fa-screwdriver-wrench",
    "bi-phone": "fa-regular fa-mobile-screen",
    "bi-bar-chart-line": "fa-regular fa-chart-line",
    "bi-globe": "fa-regular fa-globe",
}

FA_TO_BI = {v: k for k, v in BI_TO_FA.items()}


def _remap(record, mapping):
    features = record.features or []
    changed = False
    for feat in features:
        icon = feat.get("icon", "")
        if icon in mapping:
            feat["icon"] = mapping[icon]
            changed = True
    if changed:
        record.features = features
        record.save(update_fields=["features"])


def remap_to_fa(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    pms = Product.objects.filter(slug="pms").first()
    if pms:
        _remap(pms, BI_TO_FA)


def remap_back_to_bi(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    pms = Product.objects.filter(slug="pms").first()
    if pms:
        _remap(pms, FA_TO_BI)


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_seed_pms"),
    ]

    operations = [
        migrations.RunPython(remap_to_fa, remap_back_to_bi),
    ]
