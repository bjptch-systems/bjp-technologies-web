from django.db import migrations, models

ICONS = {
    "pms": "fa-regular fa-building",
    "smart-pos": "fa-regular fa-cash-register",
    "bms": "fa-regular fa-scale-balanced",
    "vikundi": "fa-regular fa-users",
}


def set_icons(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    for slug, icon in ICONS.items():
        Product.objects.filter(slug=slug, icon="").update(icon=icon)


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_smart_pos_smart_bms"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="icon",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Font Awesome icon class for the home page showcase, e.g. fa-regular fa-building",
                max_length=60,
            ),
        ),
        migrations.RunPython(set_icons, migrations.RunPython.noop),
    ]
