from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactenquiry",
            name="consent_at",
            field=models.DateTimeField(
                blank=True,
                help_text="When the visitor ticked the privacy consent box. Blank for older enquiries.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="contactenquiry",
            name="privacy_policy_version",
            field=models.CharField(
                blank=True,
                default="",
                help_text="'Last updated' date of the Privacy Policy the visitor agreed to.",
                max_length=20,
            ),
        ),
    ]
