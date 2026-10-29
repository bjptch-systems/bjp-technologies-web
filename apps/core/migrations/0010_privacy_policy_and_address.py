import datetime

from django.db import migrations, models

import apps.core.privacy_policy

OLD_ADDRESS = "Ubungo – Dar es Salaam, Tanzania"
NEW_ADDRESS = "Msakuzi, Ubungo, Dar es Salaam, 16113, Tanzania"


def update_address(apps, schema_editor):
    """Switch the live address to the full one used in the Privacy Policy. Only
    replaces the old default — never overrides a different value set in admin."""
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(pk=1, address=OLD_ADDRESS).update(address=NEW_ADDRESS)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_update_company_phone"),
    ]

    operations = [
        migrations.CreateModel(
            name="PrivacyPolicySettings",
            fields=[],
            options={
                "verbose_name": "Privacy Policy",
                "verbose_name_plural": "Privacy Policy",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="privacy_policy_body",
            field=models.TextField(
                default=apps.core.privacy_policy.default_privacy_policy,
                help_text="Full policy text in HTML (headings, paragraphs, lists, tables). Only trusted staff should edit this — it is rendered on the page as-is.",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="privacy_policy_updated",
            field=models.DateField(
                default=datetime.date.today,
                help_text="Shown as 'Last updated' on the policy page and recorded with every contact enquiry's consent. Change it whenever the policy text changes.",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address",
            field=models.CharField(
                default="Msakuzi, Ubungo, Dar es Salaam, 16113, Tanzania", max_length=200
            ),
        ),
        migrations.RunPython(update_address, migrations.RunPython.noop),
    ]
