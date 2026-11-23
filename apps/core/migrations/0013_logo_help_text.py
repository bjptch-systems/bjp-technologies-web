from django.db import migrations, models

import apps.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_about_stat_systems_delivered"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="logo",
            field=models.FileField(
                blank=True,
                help_text="Leave empty to use BJP's built-in logo (recommended). An uploaded file replaces it in both the navy header and the light footer, in its own colours, so it must read well on both. Accepted: SVG, PNG, WebP with a transparent background.",
                upload_to="branding/",
                validators=[apps.core.validators.validate_logo_file],
            ),
        ),
    ]
