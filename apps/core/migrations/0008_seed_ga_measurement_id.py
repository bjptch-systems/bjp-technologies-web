from django.db import migrations

GA_MEASUREMENT_ID = "G-C9L66H4VE4"


def seed(apps, schema_editor):
    """Pin the GA4 Measurement ID on first deploy so production starts tracking
    without anyone touching the admin. Only sets it if it is still blank — never
    overrides a value an admin has since changed."""
    SiteSettings = apps.get_model("core", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if not obj.ga_measurement_id:
        obj.ga_measurement_id = GA_MEASUREMENT_ID
        obj.save(update_fields=["ga_measurement_id"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_analyticssettings_sitesettings_ga_enabled_and_more"),
    ]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
