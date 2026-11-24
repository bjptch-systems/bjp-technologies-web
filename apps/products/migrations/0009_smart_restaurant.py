"""Smart Restaurant becomes its own product; Smart POS becomes shops-only (Nov 2026).

On the product site both run on the same system (restaurant mode of Smart POS, with a
restaurant sign-up link), so the buttons point at the matching sign-up and pages there.
Content follows bms.bjptechnologies.co.tz/smart-pos/retail and /smart-pos/restaurant.
"""

from django.db import migrations

BMS_SITE = "https://bms.bjptechnologies.co.tz"
SUPPORT_HOURS = "Mon–Fri 8 AM–6 PM, Sat 8 AM–5 PM (EAT)"
ORIGINAL_POS_TAGLINE = "Selling made simple — for shops and restaurants."

SMART_POS_SHOPS = {
    "tagline": "Selling made simple — for shops.",
    "byline": "Sales, stock and credit for shops, pharmacies, hardware stores and boutiques.",
    "live_url": f"{BMS_SITE}/smart-pos/retail",
    "short_description": (
        "Smart POS runs the till for your shop. Sell fast, know what is in stock, track who "
        "owes you and see your profit — from your phone or computer, in English or Kiswahili."
    ),
    "long_description": (
        "Smart POS is made for shops of every kind: general stores, pharmacies, hardware "
        "stores and boutiques.\n\n"
        "The till handles fast sales with printed or emailed receipts, products and services, "
        "receiving stock, and sales by weight or volume — half a kilo or a quarter litre. "
        "Credit sales show who owes you and record what they pay back, and reports show your "
        "expenses and profit daily, weekly, monthly, quarterly and yearly.\n\n"
        "You can also share your own online shop link: customers order, and you confirm."
    ),
    "problem_statements": (
        "Sales are written in a book, so nobody knows today's real takings.\n"
        "Stock goes missing and you only find out when a customer asks for it.\n"
        "Customers buy on credit and the debts are tracked from memory.\n"
        "You can't tell which products actually make a profit."
    ),
    "target_users": (
        "Shop owners — general stores, pharmacies, hardware stores and boutiques.\n"
        "Cashiers — fast sales with printed or emailed receipts.\n"
        "Storekeepers — receive stock and keep counts right.\n"
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
    ],
    "differentiators": (
        "Made for shops — pharmacies, hardware stores, boutiques and general stores.\n"
        "Sell by weight or volume as easily as by the piece.\n"
        "Works on your phone or computer, in English or Kiswahili.\n"
        "Your data is yours — your own private account, backed up every day."
    ),
    "how_it_works_steps": (
        "Start your 14-day free trial.\n"
        "Add your products and prices.\n"
        "Receive your opening stock.\n"
        "Make your first sale and check today's sales on your dashboard."
    ),
    "pricing_summary": (
        "Every plan starts with 14 days free, with no payment today. Current plans and prices "
        "are on the Smart POS website."
    ),
    "cta_primary_url": f"{BMS_SITE}/register?product=bms_shop",
    "meta_title": "Smart POS — Shop POS Software in Tanzania",
    "meta_description": (
        "Smart POS for shops, pharmacies, hardware stores and boutiques in Tanzania: fast "
        "sales, stock, credit and profit reports. English or Kiswahili. 14 days free."
    ),
    "hero_image": "products/smart-pos/hero-shops.webp",
    "og_image": "products/smart-pos/hero-shops.webp",
}

SMART_RESTAURANT = {
    "name": "Smart Restaurant",
    "slug": "smart-restaurant",
    "status": "live",
    "tagline": "From the table to the kitchen to the bill.",
    "byline": "Orders, kitchen screen, menu and bills for restaurants, cafés and hotel kitchens.",
    "live_url": f"{BMS_SITE}/smart-pos/restaurant",
    "short_description": (
        "Smart Restaurant runs your restaurant from the table to the kitchen to the bill. "
        "Waiters take orders, the kitchen sees them on screen, and the cashier closes the "
        "bill — each person sees only their own work. On your phone or computer, in English "
        "or Kiswahili."
    ),
    "long_description": (
        "Smart Restaurant is made for restaurants, cafés and hotel kitchens.\n\n"
        "Open a table, add dishes and send the order to the kitchen. Cooks see each order on "
        "the kitchen screen and mark it ready, the waiter serves, and the cashier closes the "
        "bill. Turn on the kitchen screen and cashier confirmation in Settings when you need "
        "them.\n\n"
        "Your menu holds photos and recipes, so you know the ingredient cost of every dish. "
        "Guests can order from their phone with a QR menu at the table, which staff accept "
        "first. Supplier purchases can be bought on credit and paid later, and spoiled food "
        "is written off as waste, so your profit is true."
    ),
    "problem_statements": (
        "Orders get lost between the table, the kitchen and the bill.\n"
        "You don't know what each dish really costs to make.\n"
        "Spoiled food is never recorded, so the profit figures are wrong.\n"
        "Waiters handle money without clear control."
    ),
    "target_users": (
        "Restaurant owners and managers — see orders, sales and costs in one place.\n"
        "Waiters — take orders at the table and send them to the kitchen.\n"
        "Cooks — see each order on the kitchen screen and mark it ready.\n"
        "Cashiers — confirm orders and close the bill.\n"
        "Cafés and hotel kitchens — the same tools for smaller or busier kitchens."
    ),
    "features": [
        {
            "name": "Tables and orders",
            "description": "Open a table, add dishes, send to the kitchen.",
            "icon": "fa-regular fa-utensils",
        },
        {
            "name": "Kitchen screen",
            "description": "Cooks see each order and mark it ready.",
            "icon": "fa-regular fa-tv",
        },
        {
            "name": "Cashier confirmation",
            "description": "The cashier confirms orders and closes every bill.",
            "icon": "fa-regular fa-cash-register",
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
        {
            "name": "Roles for every job",
            "description": "Waiter, Cashier, Cook and Restaurant Manager roles ready to use.",
            "icon": "fa-regular fa-user-lock",
        },
    ],
    "differentiators": (
        "Each person sees only their own work — a waiter never sees the money.\n"
        "Know the ingredient cost of every dish, and record waste so profit is true.\n"
        "Switch on the kitchen screen and cashier confirmation only when you need them.\n"
        "Works on your phone or computer, in English or Kiswahili.\n"
        "Your data is yours — your own private account, backed up every day."
    ),
    "how_it_works_steps": (
        "Start your 14-day free trial.\n"
        "Add your dishes and prices to the menu.\n"
        "Set up your tables.\n"
        "Add your staff: waiter, cashier and cook.\n"
        "Take your first order."
    ),
    "pricing_summary": (
        "Every plan starts with 14 days free, with no payment today. Current plans and prices "
        "are on the product website."
    ),
    "onboarding_promise": "14 days free — no payment today.",
    "disclosures": "",
    "cta_primary_label": "Start free trial",
    "cta_primary_url": f"{BMS_SITE}/register?product=bms_shop&business=restaurant",
    "cta_secondary_label": "See prices",
    "cta_secondary_url": f"{BMS_SITE}/pricing",
    "contact_email": "info@bjptechnologies.co.tz",
    "contact_phone": "+255 764 764 011",
    "contact_hours": SUPPORT_HOURS,
    "contact_whatsapp": "+255 764 764 011",
    "meta_title": "Smart Restaurant — Restaurant POS & Kitchen System",
    "meta_description": (
        "Smart Restaurant for restaurants, cafés and hotel kitchens in Tanzania: table "
        "orders, kitchen screen, QR menu, recipe costs and waste. 14 days free."
    ),
    "hero_image": "products/smart-restaurant/hero.webp",
    "og_image": "products/smart-restaurant/hero.webp",
    "logo_image": "products/smart-restaurant/logo.svg",
    "accent_color": "#C2410C",
    "icon": "fa-regular fa-utensils",
    "screenshots": [],
    "order": 3,
}

# PMS 1, Smart POS 2, Smart Restaurant 3, Smart BMS 4, Vikundi 5
NEW_ORDER = {"bms": (3, 4), "vikundi": (4, 5)}


def forwards(apps, schema_editor):
    Product = apps.get_model("products", "Product")

    pos = Product.objects.filter(slug="smart-pos", tagline=ORIGINAL_POS_TAGLINE).first()
    if pos:
        for field, value in SMART_POS_SHOPS.items():
            setattr(pos, field, value)
        pos.save()

    if not Product.objects.filter(slug=SMART_RESTAURANT["slug"]).exists():
        Product.objects.create(**SMART_RESTAURANT)

    for slug, (old, new) in NEW_ORDER.items():
        Product.objects.filter(slug=slug, order=old).update(order=new)


def backwards(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.filter(slug=SMART_RESTAURANT["slug"]).delete()
    for slug, (old, new) in NEW_ORDER.items():
        Product.objects.filter(slug=slug, order=new).update(order=old)


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_product_icon"),
    ]
    operations = [migrations.RunPython(forwards, backwards)]
