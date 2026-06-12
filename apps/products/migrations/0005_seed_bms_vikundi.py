"""Seed the BMS and Vikundi product records.

Content sourced from the team briefs at `bms assets/bjp-feature-brief.md`
and `vkd assets/bjp-feature-brief.md`. Decisions applied at seed time:

- Per user direction, the public site does NOT expose the live product
  URLs (demo.bjptechnologies.co.tz, vikundi.bjptechnologies.co.tz).
  Primary CTA on both routes to the BJP /contact/ form, prefilled with a
  ?product=… hint so the lead is attributed.
- Per user direction, the secondary CTA is dropped — single, clear
  "Request a demo" button.
- BMS feature icons were authored as Bootstrap Icons (`bi-*`) in the brief.
  They are remapped to Font Awesome Pro (`fa-regular fa-*`) at seed time
  because the site CSP blocks the Bootstrap Icons CDN and FA is already
  loaded site-wide (see migration 0003 for the PMS precedent).
- Vikundi keeps the brief's honest tone — the disclosures field carries
  the "single group per installation" and "share-out is proportional
  summary, not automated" notes.
- Contact email for both is info@bjptechnologies.co.tz per user direction.

Idempotent: re-running skips records that already exist by slug.
"""

from django.db import migrations

BMS_FEATURES = [
    {
        "name": "Point of Sale",
        "description": (
            "Fast counter sales with cash, card, mobile-money, bank or credit, "
            "and instant receipts."
        ),
        "icon": "fa-regular fa-cart-shopping",
    },
    {
        "name": "Inventory & Stock",
        "description": (
            "Live stock across multiple warehouses, transfers, reorder levels "
            "and low-stock alerts."
        ),
        "icon": "fa-regular fa-boxes-stacked",
    },
    {
        "name": "Invoicing & Payments",
        "description": (
            "Raise branded invoices, record part-payments and track who still owes you."
        ),
        "icon": "fa-regular fa-receipt",
    },
    {
        "name": "Sales & Quotations",
        "description": ("Quotations and sales orders that flow straight into invoices and stock."),
        "icon": "fa-regular fa-file-invoice-dollar",
    },
    {
        "name": "Purchases & Suppliers",
        "description": "Purchase orders, goods-received notes (GRN) and supplier balances.",
        "icon": "fa-regular fa-truck",
    },
    {
        "name": "Accounting & Ledger",
        "description": (
            "Chart of accounts, bank accounts, journals and petty cash — posted "
            "automatically from sales."
        ),
        "icon": "fa-regular fa-building-columns",
    },
    {
        "name": "Reports & Analytics",
        "description": "Sales trends, profit margins, top products and end-of-day summaries.",
        "icon": "fa-regular fa-chart-line",
    },
    {
        "name": "CRM & Leads",
        "description": (
            "Track leads, campaigns and a sales pipeline from first contact to won deal."
        ),
        "icon": "fa-regular fa-users",
    },
    {
        "name": "Loans / Microfinance",
        "description": (
            "Issue loans, schedule repayments and monitor overdue balances and " "portfolio risk."
        ),
        "icon": "fa-regular fa-coins",
    },
    {
        "name": "HR & Operations",
        "description": "Staff records, attendance and day-to-day operational tracking.",
        "icon": "fa-regular fa-id-badge",
    },
]

BMS_SCREENSHOTS = [
    {
        "image": "products/bms/feature-pos.png",
        "caption": "Counter POS — cash, card, mobile money, bank or credit in one screen.",
    },
    {
        "image": "products/bms/feature-inventory.png",
        "caption": "Live inventory with reorder levels and low-stock alerts across branches.",
    },
    {
        "image": "products/bms/feature-invoice.png",
        "caption": "Branded invoices with part-payment tracking and receivables.",
    },
    {
        "image": "products/bms/feature-reports.png",
        "caption": "Sales trend, profit margin and top-product reports — always live.",
    },
    {
        "image": "products/bms/feature-mobile.png",
        "caption": "Owner view from a phone — today's cash, sales and stock alerts.",
    },
]

BMS_SHORT_DESCRIPTION = (
    "BMS is an all-in-one business system for Tanzanian SMEs. Sell at the counter, "
    "track every item of stock, raise invoices, record cash, mobile-money and bank "
    "payments, and see your real profit — all in one place. Stop juggling Excel, "
    "paper books, receipts and WhatsApp orders. One login runs the whole shop."
)

BMS_LONG_DESCRIPTION = (
    "BMS (Business Management System) is a complete, web-based ERP for small and "
    "medium businesses in Tanzania — shops, wholesalers, distributors, service "
    "firms and multi-branch traders. It brings point-of-sale, inventory, invoicing, "
    "purchasing, customers, accounting and reporting into a single connected "
    "system, priced in Tanzanian Shillings and built for how local businesses "
    "actually work.\n\n"
    "Most SMEs run on a patchwork: a notebook for stock, Excel for sales, a drawer "
    "of receipts, and WhatsApp for orders. Nothing reconciles, and by month-end "
    "nobody knows what really sold or what it earned. BMS replaces that patchwork. "
    "A sale at the POS deducts stock, posts to the ledger and updates today's cash "
    "position in the same moment — so the numbers are always live and always agree.\n\n"
    "It runs in any web browser on hardware you already own — a counter PC, a "
    "cheap Android tablet, or the owner's phone — with role-based logins so staff "
    "see only what they should. The one thing BMS does better than the "
    "alternatives: it keeps stock, sales and accounting as a single source of "
    "truth, instead of three disconnected tools you have to reconcile by hand."
)

BMS_PROBLEMS = "\n".join(
    [
        "Stock runs out — or expires — without warning, because nobody tracks reorder levels.",
        "End-of-day cash never reconciles against what was actually sold.",
        "No visibility into which products and customers actually make money.",
        "Sales live in Excel, stock in a notebook, and receipts in a drawer — nothing matches.",
        "Invoices, payments and customer balances are tracked by memory, so debts get lost.",
    ]
)

BMS_TARGET_USERS = "\n".join(
    [
        "Shop & duka owners — ring up daily sales at the POS and reconcile end-of-day cash.",
        "Wholesalers & distributors — manage multi-warehouse stock, transfers and supplier purchases.",
        "Cashiers / counter staff — fast POS sales with cash, card, mobile-money or credit.",
        "Accountants & bookkeepers — pull a monthly P&L and ledger without rebuilding spreadsheets.",
        "Business managers / owners — check today's sales, stock alerts and cash from any device.",
        "Storekeepers — receive goods (GRN), track stock levels and act on low-stock alerts.",
    ]
)

BMS_DIFFERENTIATORS = "\n".join(
    [
        "Built in Tanzania, for Tanzania — Tanzanian-Shilling native, with VAT and TIN fields, not a re-skinned foreign tool you fight to localise.",
        "One source of truth — a single sale updates stock, cash and the ledger together, so unlike Excel-plus-apps your numbers can't drift apart.",
        "Records mobile-money, cash and bank — capture cash, card, mobile-money, bank-transfer and credit sales side by side.",
        "Runs on cheap hardware you own — any browser on a counter PC, Android tablet or phone; no expensive licences per seat.",
        "Multi-warehouse, role-based, bilingual-ready — stock transfers between branches, permissions per staff role, and a per-user English / Kiswahili language setting.",
    ]
)

BMS_HOW_IT_WORKS = "\n".join(
    [
        "Set up your products, opening stock and customers (or import them).",
        "Sell from the POS or raise an invoice — pick cash, mobile-money, bank or credit.",
        "Stock auto-deducts and the sale posts to your accounts in the same moment.",
        "Pull reports any time — today's cash, profit margins, top products, month-end P&L.",
    ]
)


# ─────────────────────────────────────────────────────────────────────────────


VIKUNDI_FEATURES = [
    {
        "name": "Member register & approvals",
        "description": "Register members, approve joiners, flag dormant members.",
        "icon": "fa-regular fa-users",
    },
    {
        "name": "Contributions & savings ledger",
        "description": (
            "Per-period contribution grid with entrance fee, partial-payment "
            "tracking and bulk upload."
        ),
        "icon": "fa-regular fa-piggy-bank",
    },
    {
        "name": "Loans & repayments",
        "description": (
            "Loan applications, interest, term and a full repayment schedule per member."
        ),
        "icon": "fa-regular fa-hand-holding-dollar",
    },
    {
        "name": "Fines",
        "description": "Issue and track member fines and their outstanding balances.",
        "icon": "fa-regular fa-gavel",
    },
    {
        "name": "Social / funeral fund",
        "description": "Record funeral-support disbursements for members and their dependants.",
        "icon": "fa-regular fa-heart",
    },
    {
        "name": "Mobile-money reconciliation",
        "description": "Match M-Koba mobile-money contributions to the right member.",
        "icon": "fa-regular fa-mobile-screen",
    },
    {
        "name": "Accounting & budget",
        "description": (
            "Expenses, petty cash, budgets, financial ledger, chart of accounts, "
            "journals, trial balance."
        ),
        "icon": "fa-regular fa-calculator",
    },
    {
        "name": "Reports & member statements",
        "description": (
            "Printable member financial statements plus expense, funeral and " "member analyses."
        ),
        "icon": "fa-regular fa-chart-line",
    },
    {
        "name": "Communication",
        "description": "SMS and email messaging, templates and notifications to members.",
        "icon": "fa-regular fa-comment-dots",
    },
    {
        "name": "Documents & e-signatures",
        "description": "Document library, loan documents and e-signature workflow.",
        "icon": "fa-regular fa-file-signature",
    },
    {
        "name": "Users, roles & permissions",
        "description": "Role-based access control with per-page view/create/edit/delete rights.",
        "icon": "fa-regular fa-user-shield",
    },
    {
        "name": "Audit trail",
        "description": "Every action — create, edit, approve, payout, login — logged and reviewable.",
        "icon": "fa-regular fa-clipboard-list",
    },
]

VIKUNDI_SCREENSHOTS = [
    {
        "image": "products/vikundi/feature-contribution-meeting.png",
        "caption": "The contribution-recording screen as used during a live meeting.",
    },
    {
        "image": "products/vikundi/feature-member-passbook.png",
        "caption": "A member's passbook — contributions, shares, active loan, fines.",
    },
    {
        "image": "products/vikundi/feature-loan.png",
        "caption": "Loan record with principal, interest, schedule and balance.",
    },
    {
        "image": "products/vikundi/feature-share-out.png",
        "caption": "Cycle close-out — savings-proportional share-out summary per member.",
    },
    {
        "image": "products/vikundi/feature-mobile.png",
        "caption": "A member checking their balance and contributions from a phone.",
    },
]

VIKUNDI_SHORT_DESCRIPTION = (
    "Vikundi runs your savings group the way the cashbox and record book never "
    "could. Members contribute, borrow, pay fines and support each other through "
    "the social fund — and every shilling is logged, totalled and visible. No "
    "more arguing over the book: at any moment the group knows exactly who has "
    "paid and who owes what."
)

VIKUNDI_LONG_DESCRIPTION = (
    "Vikundi is a complete management system for VICOBA (Village Community "
    "Banks), SACCOS-style savings groups and informal microfinance circles. It "
    "replaces the plastic cashbox and the hand-written record book with a "
    "single shared ledger that the chairperson, treasurer, secretary and members "
    "all see the same way — on a laptop in the meeting or on a phone at home.\n\n"
    "It is built specifically for how East African savings groups actually work: "
    "fixed-cycle contributions, an entrance fee, member loans with interest and "
    "a repayment schedule, fines, and a social/funeral fund that pays out when "
    "a member or a dependant is bereaved. Contributions paid through M-Koba "
    'mobile money are reconciled against members, so a payment is never "lost" '
    "between someone's phone and the group's books. Everything is bilingual — "
    "English and Swahili — down to the labels, statements and printed reports.\n\n"
    "The one thing it does better than paper: trust through transparency. Every "
    "create, edit, approval and payout is written to an audit trail, and any "
    "member can be handed a printed financial statement showing exactly what "
    "they have paid, what they owe and what the group has disbursed. The "
    '"the book says…" argument disappears.'
)

VIKUNDI_PROBLEMS = "\n".join(
    [
        "The cashbox can be lost, stolen, or withheld by whoever physically holds it.",
        "Hand-written record-book entries get miscounted and nobody can reconcile them later.",
        "Members argue over contribution balances and how much is still owed on a loan.",
        "Nobody has a clear, live picture of who owes what until the meeting drags on.",
        "Mobile-money (M-Koba) payments arrive but can't be tied back to a specific member.",
        "Loan repayments and interest are tracked in someone's head instead of on a schedule.",
    ]
)

VIKUNDI_TARGET_USERS = "\n".join(
    [
        "Chairperson / Mwenyekiti — runs meetings, approves members and loans, and watches the whole group from one dashboard.",
        "Treasurer / Mhazini — records and confirms contributions, fines, expenses and loan repayments; reconciles M-Koba.",
        "Secretary / Katibu — registers and approves members, keeps records, issues member statements.",
        "Members / Wanachama — check their own savings, contributions, active loan balance and fines from a phone.",
        "System administrator — manages users, roles and permissions, group settings and data backups.",
    ]
)

VIKUNDI_DIFFERENTIATORS = "\n".join(
    [
        "Built for the VICOBA model, not retrofitted accounting — contribution cycles, entrance fee, social/funeral fund and member loans are first-class, not bolted on.",
        "Genuinely bilingual EN/Swahili — every label, dashboard, statement and printed report switches between English and Swahili.",
        "Reconciles the mobile money members actually use — M-Koba contributions are tied back to the paying member instead of floating as anonymous deposits.",
        "An audit trail every member can verify — each member can be handed a printed statement, and every action is logged.",
        "Runs on low-cost infrastructure — within reach of a community group's budget.",
    ]
)

VIKUNDI_HOW_IT_WORKS = "\n".join(
    [
        "Set up the group — register members (one-by-one or bulk import) and approve them.",
        "Set the rules — contribution cycle and amount, entrance fee, loan interest, fines and the social-fund position in Group Settings.",
        "Record at each meeting — capture contributions (cash, bank or M-Koba), fines, loans and repayments; the treasurer confirms pending entries.",
        "Report any time — print a member's financial statement or the group's reports, and at cycle end produce a savings-proportional share-out summary.",
    ]
)

VIKUNDI_DISCLOSURES = "\n".join(
    [
        "Single group per installation today — multi-group / federation oversight from one dashboard is not yet shipped.",
        "Cycle close-out is produced as a savings-proportional summary; a one-click automated share-out engine is on the roadmap, not in the build.",
    ]
)


def seed(apps, schema_editor):
    Product = apps.get_model("products", "Product")

    if not Product.objects.filter(slug="bms").exists():
        Product.objects.create(
            name="BMS — Business Management System",
            slug="bms",
            tagline="Run your whole business from one screen.",
            byline="An all-in-one ERP built in Tanzania for Tanzanian SMEs and retailers.",
            live_url="",
            status="live",
            short_description=BMS_SHORT_DESCRIPTION,
            long_description=BMS_LONG_DESCRIPTION,
            problem_statements=BMS_PROBLEMS,
            target_users=BMS_TARGET_USERS,
            features=BMS_FEATURES,
            differentiators=BMS_DIFFERENTIATORS,
            how_it_works_steps=BMS_HOW_IT_WORKS,
            pricing_summary="",
            onboarding_promise=(
                "From signup to your first recorded sale in under one hour, with "
                "your products and opening stock loaded for you."
            ),
            cta_primary_label="Request a demo",
            cta_primary_url="/contact/?product=bms",
            cta_secondary_label="",
            cta_secondary_url="",
            contact_email="info@bjptechnologies.co.tz",
            meta_title="BMS — Business Management System for Tanzanian SMEs",
            meta_description=(
                "All-in-one Tanzanian ERP: POS, inventory, invoicing, mobile-money "
                "payments and accounting in one system. Run your whole business "
                "from one screen."
            ),
            hero_image="products/bms/hero-dashboard.png",
            og_image="products/bms/og-card.png",
            logo_image="products/bms/logo.svg",
            accent_color="#0D6EFD",
            screenshots=BMS_SCREENSHOTS,
            order=2,
        )

    if not Product.objects.filter(slug="vikundi").exists():
        Product.objects.create(
            name="Vikundi — VICOBA Management System",
            slug="vikundi",
            tagline="VICOBA, finally without the cashbox.",
            byline="Digital savings groups built for Tanzanian communities.",
            live_url="",
            status="live",
            short_description=VIKUNDI_SHORT_DESCRIPTION,
            long_description=VIKUNDI_LONG_DESCRIPTION,
            problem_statements=VIKUNDI_PROBLEMS,
            target_users=VIKUNDI_TARGET_USERS,
            features=VIKUNDI_FEATURES,
            differentiators=VIKUNDI_DIFFERENTIATORS,
            how_it_works_steps=VIKUNDI_HOW_IT_WORKS,
            pricing_summary="",
            onboarding_promise=(
                "From group registration to your first recorded contribution in "
                "under 30 minutes."
            ),
            disclosures=VIKUNDI_DISCLOSURES,
            cta_primary_label="Request a demo",
            cta_primary_url="/contact/?product=vikundi",
            cta_secondary_label="",
            cta_secondary_url="",
            contact_email="info@bjptechnologies.co.tz",
            meta_title="Vikundi — VICOBA Management System for Tanzania",
            meta_description=(
                "Run your VICOBA without the cashbox. Vikundi digitises member "
                "savings, loans, fines and share-out — bilingual English & Swahili."
            ),
            hero_image="products/vikundi/hero-dashboard.png",
            og_image="products/vikundi/og-card.png",
            logo_image="products/vikundi/logo.svg",
            accent_color="#0D6EFD",
            screenshots=VIKUNDI_SCREENSHOTS,
            order=3,
        )


def unseed(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.filter(slug__in=["bms", "vikundi"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_product_disclosures"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
