from django.db import migrations, models

INSTAGRAM_URL = "https://www.instagram.com/bjptechnologies/"

# field -> (old phrase, new phrase). Applied only while the old phrase is still present.
PHRASES = {
    "hero_subtext": (
        "tailored software, cybersecurity, cloud, and payment integration solutions",
        "tailored software, bulk SMS, and payment integration solutions",
    ),
    "about_body": (
        "the software, infrastructure, and security systems that",
        "the software, payment and communication systems that",
    ),
    "about_intro": (
        "custom software development and cloud infrastructure to cybersecurity and managed IT",
        "custom software development and payment integrations to bulk SMS and managed IT",
    ),
    "about_what_we_do": (
        "From secure web applications to cloud infrastructure and mobile money",
        "From secure web applications to bulk SMS and mobile money",
    ),
    "services_banner_subtext": (
        "From custom software to cloud infrastructure —",
        "From custom software to bulk SMS —",
    ),
}


def forwards(apps, schema_editor):
    """Add the Instagram link and drop cloud/cybersecurity wording from site texts,
    never overriding values an admin has already changed."""
    SiteSettings = apps.get_model("core", "SiteSettings")
    site, _ = SiteSettings.objects.get_or_create(pk=1)
    changed = []
    if not site.instagram_url:
        site.instagram_url = INSTAGRAM_URL
        changed.append("instagram_url")
    for field, (old, new) in PHRASES.items():
        value = getattr(site, field)
        if old in value:
            setattr(site, field, value.replace(old, new))
            changed.append(field)
    if changed:
        site.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_privacy_policy_and_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="google_site_verification",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Search Console 'HTML tag' verification code — only the content value, e.g. abc123XYZ. Leave blank once verified another way.",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="instagram_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="about_body",
            field=models.TextField(
                default="BJP Technologies (T) Limited is a full-service IT company headquartered in Ubungo, Dar es Salaam. We build and maintain the software, payment and communication systems that keep growing businesses running — from Tanzanian startups to regional enterprises."
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="about_intro",
            field=models.TextField(
                default="BJP Technologies (T) Limited is a Tanzanian IT solutions company headquartered in Ubungo, Dar es Salaam. We deliver enterprise-grade technology services — from custom software development and payment integrations to bulk SMS and managed IT — helping businesses across East Africa grow securely and operate at scale."
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="about_what_we_do",
            field=models.TextField(
                default="We bring together the technology, expertise, and support businesses need to solve real problems. From secure web applications to bulk SMS and mobile money payment integrations — we cover the full technology stack so our clients can focus on growth."
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="hero_subtext",
            field=models.TextField(
                default="Tanzania's trusted IT partner — delivering tailored software, bulk SMS, and payment integration solutions that drive real business growth."
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="services_banner_subtext",
            field=models.TextField(
                default="From custom software to bulk SMS — we deliver secure, scalable technology that helps businesses across East Africa grow with confidence."
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="google_maps_url",
            field=models.URLField(
                default="https://www.google.com/maps?cid=17710749172499910700",
                help_text=(
                    "Link to the BJP Business Profile on Google Maps. Used by the 'Get "
                    "directions' button and the business details Google reads from the site."
                ),
                max_length=300,
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
