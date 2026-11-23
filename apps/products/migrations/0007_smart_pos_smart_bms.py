"""Release 2 (Nov 2026): BMS becomes Smart BMS, and Smart POS is added.

Content follows the live product site (bms.bjptechnologies.co.tz). Claims that site does
not make — mobile money, VAT/TIN fields, low-stock alerts — are left out on purpose.
No screenshots: BJP has no real product screenshots yet, and mock-ups are not shown as
the real product.
"""

from django.db import migrations

BMS_SITE = "https://bms.bjptechnologies.co.tz"
SUPPORT_HOURS = "Mon–Fri 8 AM–6 PM, Sat 8 AM–5 PM (EAT)"

SMART_BMS = {
    "name": "Smart BMS",
    "tagline": "Real accounting, with your whole business connected.",
    "byline": "Full accounting, sales, purchases, HR and payroll for growing companies.",
    "live_url": f"{BMS_SITE}/smart-bms",
    "short_description": (
        "Smart BMS is the complete business management system for growing companies. "
        "Every sale, purchase, payment and payslip posts to one double-entry ledger, so your "
        "Trial Balance, Profit & Loss and Balance Sheet always agree. Works on phone or "
        "computer, in English or Kiswahili."
    ),
    "long_description": (
        "Smart BMS brings every department of your company into one set of books: "
        "accounting, sales, purchases, banks and expenses, HR and payroll, plus projects, "
        "assets and CRM. A Point of Sale is included.\n\n"
        "Because every transaction posts to the same double-entry ledger, your reports are "
        "always ready — Trial Balance, Profit & Loss, Balance Sheet and Cash Flow — without "
        "rebuilding spreadsheets at month-end.\n\n"
        "It is made for business owners as well as accountants, in English or Kiswahili. "
        "Each staff member sees only the work their role needs, and every company has its "
        "own private database, backed up every day."
    ),
    "problem_statements": (
        "Sales, purchases and payroll live in different files, so the books never quite agree.\n"
        "Month-end reports take days of rebuilding spreadsheets.\n"
        "Owners can't see the real financial position without waiting for the accountant.\n"
        "Staff records and payslips are kept by hand."
    ),
    "target_users": (
        "Company owners and directors — see the real financial position any time.\n"
        "Accountants and bookkeepers — journals and full financial reports in one place.\n"
        "HR and payroll staff — staff records, payslips and payroll.\n"
        "Sales and purchasing teams — quotations, invoices, suppliers and bills."
    ),
    "features": [
        {
            "name": "Accounting",
            "description": "Chart of accounts, journals, Trial Balance, Profit & Loss, "
            "Balance Sheet and Cash Flow.",
            "icon": "fa-regular fa-scale-balanced",
        },
        {
            "name": "Sales",
            "description": "Quotations, invoices and customer payments.",
            "icon": "fa-regular fa-file-invoice",
        },
        {
            "name": "Purchases",
            "description": "Suppliers, bills and warehouses.",
            "icon": "fa-regular fa-truck",
        },
        {
            "name": "Banks and expenses",
            "description": "Every shilling in and out recorded against your bank accounts.",
            "icon": "fa-regular fa-building-columns",
        },
        {
            "name": "HR and payroll",
            "description": "Staff records, payslips and payroll.",
            "icon": "fa-regular fa-users",
        },
        {
            "name": "Projects, assets and CRM",
            "description": "Track projects, company assets and customer relationships.",
            "icon": "fa-regular fa-diagram-project",
        },
        {
            "name": "Point of Sale included",
            "description": "Sell at the counter, with every sale posted straight to the books.",
            "icon": "fa-regular fa-cash-register",
        },
        {
            "name": "Roles and permissions",
            "description": "Each staff member sees only the work their role needs.",
            "icon": "fa-regular fa-user-lock",
        },
    ],
    "differentiators": (
        "One double-entry ledger — sales, purchases, payments and payslips all post to the "
        "same books, so the reports always agree.\n"
        "Made for owners, not only accountants — in English or Kiswahili.\n"
        "Your data is yours — every company has its own private database, backed up every day.\n"
        "BJP reviews every Smart BMS account before it opens, so you start set up properly."
    ),
    "how_it_works_steps": (
        "Start your 14-day free trial — BJP reviews and opens your account.\n"
        "Review your chart of accounts.\n"
        "Add your customers and suppliers.\n"
        "Create your first invoice.\n"
        "Add your staff and their roles."
    ),
    "pricing_summary": (
        "Every plan starts with 14 days free, with no payment today. Current plans and prices "
        "are on the Smart BMS website."
    ),
    "onboarding_promise": "14 days free — no payment today.",
    "disclosures": "",
    "cta_primary_label": "Start free trial",
    "cta_primary_url": f"{BMS_SITE}/register?product=bms_full",
    "cta_secondary_label": "See prices",
    "cta_secondary_url": f"{BMS_SITE}/pricing",
    "contact_email": "info@bjptechnologies.co.tz",
    "contact_phone": "+255 764 764 011",
    "contact_hours": SUPPORT_HOURS,
    "contact_whatsapp": "+255 764 764 011",
    "meta_title": "Smart BMS — Accounting, HR & Payroll Software",
    "meta_description": (
        "Smart BMS: full accounting, Trial Balance, sales, purchases, HR and payroll for "
        "growing companies in Tanzania. English or Kiswahili. 14 days free."
    ),
    "hero_image": "products/bms/smart-bms-hero.webp",
    "og_image": "products/bms/smart-bms-hero.webp",
    "logo_image": "products/bms/smart-bms-logo.svg",
    "screenshots": [],
    "order": 3,
}

SMART_POS = {
    "name": "Smart POS",
    "slug": "smart-pos",
    "status": "live",
    "tagline": "Selling made simple — for shops and restaurants.",
    "byline": "Sales, stock and credit for shops and restaurants, on your phone or computer.",
    "live_url": f"{BMS_SITE}/smart-pos",
    "short_description": (
        "Smart POS runs the till for shops and restaurants. Sell fast, know what is in stock, "
        "track who owes you and see your profit — or take orders from the table to the "
        "kitchen to the bill. On your phone or computer, in English or Kiswahili."
    ),
    "long_description": (
        "Smart POS works the way you sell. Choose Retail for shops, pharmacies, hardware "
        "stores and boutiques, or Restaurant for restaurants, cafés and hotel kitchens. The "
        "plans are the same for both.\n\n"
        "In a shop, the till handles fast sales with printed or emailed receipts, stock and "
        "receiving, sales by weight or volume, credit sales and daily to yearly profit "
        "reports. You can even share an online shop link so customers order and you confirm.\n\n"
        "In a restaurant, waiters take orders, the kitchen sees them on screen, and the "
        "cashier closes the bill. Each person sees only their own work — a waiter never sees "
        "the money."
    ),
    "problem_statements": (
        "Sales are written in a book, so nobody knows today's real takings.\n"
        "Stock goes missing and you only find out when a customer asks for it.\n"
        "Customers buy on credit and the debts are tracked from memory.\n"
        "Restaurant orders get lost between the table, the kitchen and the bill."
    ),
    "target_users": (
        "Shop owners — shops, pharmacies, hardware stores and boutiques.\n"
        "Restaurants, cafés and hotel kitchens — tables, kitchen and bill in one system.\n"
        "Cashiers — fast sales with printed or emailed receipts.\n"
        "Waiters and cooks — each sees only their own orders.\n"
        "Owners on the move — check today's sales from the phone."
    ),
    "features": [
        {
            "name": "Fast selling",
            "description": "Printed or emailed receipts in seconds.",
            "icon": "fa-regular fa-cash-register",
        },
        {
            "name": "Stock you can trust",
            "description": "Products, services and receiving stock.",
            "icon": "fa-regular fa-boxes-stacked",
        },
        {
            "name": "Sell by weight or volume",
            "description": "Half a kilo, a quarter litre — the till takes it.",
            "icon": "fa-regular fa-scale-unbalanced",
        },
        {
            "name": "Credit sales",
            "description": "See who owes you and record what they pay back.",
            "icon": "fa-regular fa-hand-holding-dollar",
        },
        {
            "name": "Expenses and profit",
            "description": "Daily, weekly, monthly, quarterly and yearly reports.",
            "icon": "fa-regular fa-chart-line",
        },
        {
            "name": "Your own online shop",
            "description": "Share a link; customers order, you confirm.",
            "icon": "fa-regular fa-store",
        },
        {
            "name": "Tables and orders",
            "description": "Restaurant mode: open a table, add dishes, send to the kitchen.",
            "icon": "fa-regular fa-utensils",
        },
        {
            "name": "Kitchen screen",
            "description": "Cooks see each order and mark it ready.",
            "icon": "fa-regular fa-display",
        },
        {
            "name": "Menu with recipes",
            "description": "Photos, recipes and the ingredient cost of every dish.",
            "icon": "fa-regular fa-book-open",
        },
        {
            "name": "QR menu at the table",
            "description": "Guests order from their phone; staff accept first.",
            "icon": "fa-regular fa-qrcode",
        },
        {
            "name": "Buy on credit, pay later",
            "description": "Supplier purchases you settle when you are ready.",
            "icon": "fa-regular fa-file-invoice-dollar",
        },
        {
            "name": "Waste recorded",
            "description": "Spoiled food is written off, so your profit is true.",
            "icon": "fa-regular fa-trash-can",
        },
    ],
    "differentiators": (
        "One system for shops and restaurants — choose Retail or Restaurant when you sign up.\n"
        "Each person sees only their own work — a waiter never sees the money.\n"
        "Works on your phone or computer, in English or Kiswahili.\n"
        "Your data is yours — your own private account, backed up every day."
    ),
    "how_it_works_steps": (
        "Start your 14-day free trial and choose Retail or Restaurant.\n"
        "Add your products and prices — or your menu and tables.\n"
        "Add your staff and their roles.\n"
        "Make your first sale and check today's sales on your dashboard."
    ),
    "pricing_summary": (
        "Every plan starts with 14 days free, with no payment today. The plans are the same "
        "for shops and restaurants; current prices are on the Smart POS website."
    ),
    "onboarding_promise": "14 days free — no payment today.",
    "disclosures": "",
    "cta_primary_label": "Start free trial",
    "cta_primary_url": f"{BMS_SITE}/register?product=bms_shop",
    "cta_secondary_label": "See prices",
    "cta_secondary_url": f"{BMS_SITE}/pricing",
    "contact_email": "info@bjptechnologies.co.tz",
    "contact_phone": "+255 764 764 011",
    "contact_hours": SUPPORT_HOURS,
    "contact_whatsapp": "+255 764 764 011",
    "meta_title": "Smart POS — Shop & Restaurant POS Software",
    "meta_description": (
        "Smart POS for shops and restaurants in Tanzania: sales, stock, credit, kitchen "
        "orders and QR menus. Phone or computer, English or Kiswahili. 14 days free."
    ),
    "hero_image": "products/smart-pos/hero.webp",
    "og_image": "products/smart-pos/hero.webp",
    "logo_image": "products/smart-pos/logo.svg",
    "accent_color": "#0B6FC7",
    "screenshots": [],
    "order": 2,
}

ORIGINAL_BMS_NAME = "BMS — Business Management System"


def forwards(apps, schema_editor):
    Product = apps.get_model("products", "Product")

    # Rewrite BMS only while it is still the originally seeded product.
    bms = Product.objects.filter(slug="bms", name=ORIGINAL_BMS_NAME).first()
    if bms:
        for field, value in SMART_BMS.items():
            setattr(bms, field, value)
        bms.save()

    if not Product.objects.filter(slug=SMART_POS["slug"]).exists():
        Product.objects.create(**SMART_POS)

    # Vikundi moves after the two BJP business products (PMS 1, Smart POS 2, Smart BMS 3).
    Product.objects.filter(slug="vikundi", order=3).update(order=4)


def backwards(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.filter(slug=SMART_POS["slug"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_drop_bms_loans_feature"),
    ]
    operations = [migrations.RunPython(forwards, backwards)]
