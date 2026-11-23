import django.db.models.deletion
from django.db import migrations, models


def feature_smart_pos(apps, schema_editor):
    """Retail & Wholesale recommends Smart POS (only if nothing is set yet)."""
    Industry = apps.get_model("industries", "Industry")
    Product = apps.get_model("products", "Product")
    smart_pos = Product.objects.filter(slug="smart-pos").first()
    if smart_pos:
        Industry.objects.filter(slug="retail-wholesale", featured_product__isnull=True).update(
            featured_product=smart_pos
        )


class Migration(migrations.Migration):

    dependencies = [
        ("industries", "0003_remove_cloud_security_wording"),
        ("products", "0007_smart_pos_smart_bms"),
    ]

    operations = [
        migrations.AddField(
            model_name="industry",
            name="featured_product",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional BJP product recommended on this industry's page.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="featured_in_industries",
                to="products.product",
            ),
        ),
        migrations.RunPython(feature_smart_pos, migrations.RunPython.noop),
    ]
