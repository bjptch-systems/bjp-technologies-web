from django.db import migrations, models


def relabel(apps, schema_editor):
    """Cybersecurity is paused, so the About counter no longer advertises security
    audits. Only changes the label while it still has the old default."""
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(pk=1, about_stat_3_label="Security Audits Done").update(
        about_stat_3_label="Systems Delivered"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_instagram_search_console_service_wording"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="about_stat_3_label",
            field=models.CharField(default="Systems Delivered", max_length=60),
        ),
        migrations.RunPython(relabel, migrations.RunPython.noop),
    ]
