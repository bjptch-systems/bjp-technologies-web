"""LMS — Loan Management System joins the products (Nov 2026).

Content follows the module descriptions inside lms.bjptechnologies.co.tz. Each install
is set up per client, so there is no public sign-up: the button books a demo through
the contact form and pricing is on request. The credit-bureau, banking and
payment-gateway links are not advertised until one is confirmed connected.
"""

from django.db import migrations

SUPPORT_HOURS = "Mon–Fri 8 AM–6 PM, Sat 8 AM–5 PM (EAT)"

LMS = {
    "name": "LMS — Loan Management System",
    "slug": "lms",
    "status": "live",
    "tagline": "Every loan, from application to the last shilling.",
    "byline": "Loans, savings, collections and accounts for microfinance, SACCOS and lenders.",
    "live_url": "",
    "short_description": (
        "LMS runs a lending business from one place: customers and guarantors, loan "
        "applications and collateral, repayments and arrears, member savings and shares, "
        "and the accounts behind them — with the reports your board and regulator ask for."
    ),
    "long_description": (
        "LMS is made for microfinance institutions, SACCOS, VICOBA and money lenders in "
        "Tanzania.\n\n"
        "Register customers with their KYC and NIDA details, add guarantors and collateral, "
        "and take each loan from application to disbursement. Repayments can be recorded one "
        "by one, or in bulk: upload a bank or mobile-money statement, check every line, then "
        "post them all. Overdue loans are listed with reminders, and loans can be "
        "restructured, charged, written off and recovered — each step posted to the books.\n\n"
        "Member savings, shares and staff portfolios sit alongside the loans, and the "
        "accounting is built in: journals, expenses, budget, petty cash, bank reconciliation, "
        "income statement, balance sheet, trial balance and cash flow."
    ),
    "problem_statements": (
        "Loan records live in spreadsheets and nobody trusts the arrears figure.\n"
        "Repayments arrive by bank and mobile money and take days to match by hand.\n"
        "Loan officers' field visits and portfolios are hard to follow up.\n"
        "Month-end accounts and regulatory reports are prepared by hand."
    ),
    "target_users": (
        "Microfinance institutions — the full loan book, branches and staff portfolios.\n"
        "SACCOS — member savings, shares and loans in one register.\n"
        "VICOBA and money lenders — simple loans with guarantors and collateral.\n"
        "Loan officers — applications, field visits and collections.\n"
        "Accountants and managers — the books, reports and audit trail."
    ),
    "features": [
        {
            "name": "Loan applications",
            "description": "From application to disbursement, with guarantors and collateral.",
            "icon": "fa-regular fa-file-invoice-dollar",
        },
        {
            "name": "Bulk repayments",
            "description": "Upload a bank or mobile-money statement, check, then post every line.",
            "icon": "fa-regular fa-mobile-screen",
        },
        {
            "name": "Arrears and collections",
            "description": "Overdue loans, reminders, restructuring, write-offs and recoveries.",
            "icon": "fa-regular fa-hand-holding-dollar",
        },
        {
            "name": "Savings and shares",
            "description": "Compulsory and voluntary savings, share purchases and statements.",
            "icon": "fa-regular fa-piggy-bank",
        },
        {
            "name": "Accounting built in",
            "description": "Journals, expenses, budget, petty cash and bank reconciliation.",
            "icon": "fa-regular fa-calculator",
        },
        {
            "name": "Reports and provisioning",
            "description": "Portfolio, delinquency, loan-loss provisioning and financial statements.",
            "icon": "fa-regular fa-chart-line",
        },
        {
            "name": "Field visits and portfolios",
            "description": "Loan officers' appraisal, monitoring and recovery visits.",
            "icon": "fa-regular fa-users",
        },
        {
            "name": "Ask LMS",
            "description": "Ask about your loan book in plain language.",
            "icon": "fa-regular fa-comment-dots",
        },
    ],
    "differentiators": (
        "Every loan action — charge, restructure, write-off, recovery — is posted to the books.\n"
        "Bulk repayments from bank and mobile-money statements, checked before posting.\n"
        "Loans, savings, shares and accounting in one system, not four.\n"
        "Audit logs and login history for every user.\n"
        "Set up and supported by BJP in Dar es Salaam."
    ),
    "how_it_works_steps": (
        "Book a demo and tell us how you lend.\n"
        "We set up your branches, interest rates and charges.\n"
        "Bring in your customers and running loans.\n"
        "Train your staff and start recording repayments."
    ),
    "pricing_summary": "Price on request — depends on your branches and number of users.",
    "onboarding_promise": "",
    "disclosures": "",
    "cta_primary_label": "Book a demo",
    "cta_primary_url": "/contact/?product=lms",
    "cta_secondary_label": "",
    "cta_secondary_url": "",
    "contact_email": "info@bjptechnologies.co.tz",
    "contact_phone": "+255 764 764 011",
    "contact_hours": SUPPORT_HOURS,
    "contact_whatsapp": "+255 764 764 011",
    "meta_title": "LMS — Loan Management System for Microfinance & SACCOS",
    "meta_description": (
        "LMS for microfinance, SACCOS and lenders in Tanzania: loan applications, bulk "
        "repayments, arrears, savings, shares, accounting and reports. Book a demo."
    ),
    "hero_image": "products/lms/hero.webp",
    "og_image": "products/lms/hero.webp",
    "logo_image": "products/lms/logo.svg",
    "accent_color": "#6D28D9",
    "icon": "fa-regular fa-hand-holding-dollar",
    "screenshots": [],
    "order": 6,
}


def forwards(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    if not Product.objects.filter(slug=LMS["slug"]).exists():
        Product.objects.create(**LMS)


def backwards(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.filter(slug=LMS["slug"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0009_smart_restaurant"),
    ]
    operations = [migrations.RunPython(forwards, backwards)]
