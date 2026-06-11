"""Seed the PMS (Property Management System) product record.

Content is sourced from the BJP feature brief produced by the PMS team
(pms details/bjp-feature-brief.md). Idempotent: re-running does nothing
if a product with slug 'pms' already exists.
"""

from django.db import migrations

PMS_FEATURES = [
    {
        "name": "Property & unit inventory",
        "description": (
            "Organise buildings, apartments, shops, offices and business frames by location."
        ),
        "icon": "bi-buildings",
    },
    {
        "name": "Renters & leases",
        "description": (
            "Keep renter records and lease contracts, with deposits, billing cycles and renewals."
        ),
        "icon": "bi-file-earmark-text",
    },
    {
        "name": "Invoicing & receipts",
        "description": "Generate branded PDF invoices and automatic receipts in TSh.",
        "icon": "bi-receipt",
    },
    {
        "name": "Payment tracking",
        "description": (
            "Record M-Pesa, Tigo Pesa, Airtel Money, bank and cash payments against each invoice."
        ),
        "icon": "bi-cash-coin",
    },
    {
        "name": "Maintenance tracking",
        "description": "Log, assign, prioritise and cost-track repair requests to completion.",
        "icon": "bi-tools",
    },
    {
        "name": "Renter self-service portal",
        "description": "A mobile-friendly login where renters see balances and report issues.",
        "icon": "bi-phone",
    },
    {
        "name": "Reports & exports",
        "description": (
            "Collection trends, occupancy, arrears and profit — exportable to PDF or Excel."
        ),
        "icon": "bi-bar-chart-line",
    },
    {
        "name": "Built-in landlord website",
        "description": (
            "A CMS-managed public page per landlord with vacant-unit listings and a contact form."
        ),
        "icon": "bi-globe",
    },
]

PMS_SCREENSHOTS = [
    {
        "image": "products/pms/feature-invoice.png",
        "caption": "Branded TSh invoice — generated automatically from each lease.",
    },
    {
        "image": "products/pms/feature-maintenance.png",
        "caption": "Maintenance request tracking — log, assign and cost-track to completion.",
    },
    {
        "image": "products/pms/feature-mobile-renter.png",
        "caption": "Renter self-service portal — balances and maintenance from a phone.",
    },
    {
        "image": "products/pms/feature-reports.png",
        "caption": "Monthly rent-collection report — exportable to PDF or Excel.",
    },
]

PMS_SHORT_DESCRIPTION = (
    "PMS is browser-based property-management software for Tanzanian landlords and "
    "managing agents. Track properties, units, renters and leases, raise branded "
    "invoices in TSh, record M-Pesa, Tigo Pesa, Airtel Money, bank and cash payments, "
    "and let renters check what they owe online. One platform serves many landlords, "
    "in English or Swahili."
)

PMS_LONG_DESCRIPTION = (
    "PMS (Property Management System) is a single platform where a landlord, a managing "
    "agent or their staff run an entire rental business from a browser. Properties, units, "
    "renters, leases, invoices, payments, receipts and maintenance all live in one place — "
    "no installs, no spreadsheets, and nothing lost in a WhatsApp thread.\n\n"
    "It is built specifically for the Tanzanian market. Money is handled in Tanzanian "
    "Shillings (with USD supported for commercial leases), phone numbers follow the local "
    "format, and payments cover the channels landlords actually use — M-Pesa, Tigo Pesa, "
    "Airtel Money, HaloPesa, bank transfer and cash. It handles both residential apartments "
    'and commercial spaces, including the "business frames" let to traders in markets '
    "like Kariakoo. Every screen is bilingual: English by default, switchable to Swahili "
    "anywhere.\n\n"
    "The one thing PMS does better than a notebook, an Excel sheet or a WhatsApp chat: it "
    "always knows who has paid, who owes, and since when. Invoices go out branded and "
    "consistent, receipts are generated automatically, arrears are visible at a glance, and "
    "renters get their own portal to see balances and raise maintenance — so the landlord "
    'stops fielding "how much do I owe?" calls and starts seeing the whole portfolio on '
    "one dashboard."
)

PMS_PROBLEMS = "\n".join(
    [
        "Rent is tracked in notebooks, Excel or WhatsApp, so arrears quietly slip through the cracks.",
        "No single source of truth for who paid, who still owes, and since which month.",
        "Invoices and receipts are handwritten, inconsistent and unbranded.",
        "Maintenance requests get lost in phone calls and chats, with no record of cost or status.",
        "Renters have no way to check their own balance, so the landlord answers the same questions all day.",
    ]
)

PMS_TARGET_USERS = "\n".join(
    [
        "Landlords / property owners — track rent, arrears and occupancy across all their properties from one dashboard.",
        "Managing agents / property managers — run several landlords' portfolios, each in its own isolated workspace, from one platform.",
        "Property staff (caretakers, accountants) — record payments, issue receipts and log maintenance without touching the books directly.",
        "Renters / wapangaji — sign in to a self-service portal to view invoices, see what they owe and raise maintenance requests.",
        "Commercial & business-frame tenants — track shop, office and Kariakoo-style frame rentals alongside residential units.",
    ]
)

PMS_DIFFERENTIATORS = "\n".join(
    [
        "Truly bilingual — every label is English or Swahili, switchable anywhere, anytime.",
        "Built locally for Tanzania — TSh currency, local phone formats, NIDA/TIN fields, and the mobile-money channels landlords actually use.",
        "Browser-based & low-bandwidth friendly — nothing to install; works on a phone or a basic laptop.",
        "Residential and commercial — handles apartments, offices, shops and Kariakoo-style business frames in the same system.",
        "One platform, many landlords — each client gets an isolated, secure workspace, so a managing agent can run multiple portfolios.",
    ]
)

PMS_HOW_IT_WORKS = "\n".join(
    [
        "Add your properties and units — buildings, apartments, shops or frames, grouped by location.",
        "Add renters and create leases — set the rent, deposit and billing cycle.",
        "Issue invoices and record payments — bill monthly and log each payment as it arrives; receipts generate automatically.",
        "Renters self-serve — they check balances and raise maintenance from their own portal, while you watch the whole portfolio on one dashboard.",
    ]
)


def seed_pms(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    if Product.objects.filter(slug="pms").exists():
        return

    Product.objects.create(
        name="PMS by BJP Technologies",
        slug="pms",
        tagline="Property management, finally simple.",
        byline="Multi-tenant rental and lease management built for the Tanzanian market.",
        live_url="https://pms.bjptechnologies.co.tz",
        status="live",
        short_description=PMS_SHORT_DESCRIPTION,
        long_description=PMS_LONG_DESCRIPTION,
        problem_statements=PMS_PROBLEMS,
        target_users=PMS_TARGET_USERS,
        features=PMS_FEATURES,
        differentiators=PMS_DIFFERENTIATORS,
        how_it_works_steps=PMS_HOW_IT_WORKS,
        pricing_summary=(
            "Pricing depends on portfolio size (number of properties, units and staff logins). "
            "It is quoted after a short demo so the plan matches the landlord's scale."
        ),
        onboarding_promise=(
            "We set up your workspace and help you import your first properties within 24 hours."
        ),
        cta_primary_label="Request a demo",
        cta_primary_url="https://pms.bjptechnologies.co.tz",
        cta_secondary_label="Take the tour",
        cta_secondary_url="https://pms.bjptechnologies.co.tz",
        meta_title="PMS — Property Management Software for Tanzania",
        meta_description=(
            "Browser-based property management for Tanzanian landlords. Track rent, leases, "
            "invoices & maintenance in TSh — bilingual EN/Swahili. Request a demo."
        ),
        hero_image="products/pms/hero-dashboard.png",
        og_image="products/pms/og-card.png",
        logo_image="products/pms/logo.svg",
        accent_color="#0F766E",
        screenshots=PMS_SCREENSHOTS,
        order=1,
    )


def unseed_pms(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.filter(slug="pms").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_pms, unseed_pms),
    ]
