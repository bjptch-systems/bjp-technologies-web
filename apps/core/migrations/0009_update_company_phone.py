from django.db import migrations, models

OLD_PHONE = "+255 678 290 994"
NEW_PHONE = "+255 764 764 011"


def _digits(value):
    return "".join(ch for ch in value if ch.isdigit())


def update_phone(apps, schema_editor):
    """Switch the live company phone to the new number on deploy. Only replaces
    the old number (in any spacing) — never overrides a different value an
    admin has since set."""
    SiteSettings = apps.get_model("core", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if _digits(obj.phone)[-9:] == _digits(OLD_PHONE)[-9:]:
        obj.phone = NEW_PHONE
        obj.save(update_fields=["phone"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_seed_ga_measurement_id"),
    ]
    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="phone",
            field=models.CharField(default=NEW_PHONE, max_length=30),
        ),
        migrations.RunPython(update_phone, migrations.RunPython.noop),
    ]
