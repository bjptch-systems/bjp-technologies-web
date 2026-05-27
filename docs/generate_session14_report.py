"""Generate BJP Technologies Session 14 Report PDF — Google Analytics 4 integration."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = "docs/BJP_Technologies_Session14_Report.pdf"

NAVY = colors.HexColor("#0D1B4B")
BLUE = colors.HexColor("#1565C0")
CYAN = colors.HexColor("#00C6FF")
GREY = colors.HexColor("#8A94B0")
OFF_WHITE = colors.HexColor("#F4F6FC")
GREEN = colors.HexColor("#2ECC71")
WHITE = colors.white
BLACK = colors.black
LIGHT_GREY = colors.HexColor("#E8ECF4")

PAGE_W, PAGE_H = A4
CONTENT_W = 174 * mm


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 18 * mm, PAGE_W, 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(0, PAGE_H - 19.5 * mm, PAGE_W, 1.5 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(18 * mm, PAGE_H - 12 * mm, "BJP TECHNOLOGIES (T) LIMITED")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - 18 * mm, PAGE_H - 12 * mm, "SESSION 14 — WORK REPORT")

    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(0, 12 * mm, PAGE_W, 1 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(
        18 * mm, 4.5 * mm, "bjptechnologies.co.tz  |  Secure Technology. Scalable Growth."
    )
    canvas.drawRightString(PAGE_W - 18 * mm, 4.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(0, PAGE_H * 0.38, PAGE_W, 2 * mm, fill=1, stroke=0)
    canvas.rect(0, PAGE_H * 0.38 - 4 * mm, PAGE_W, 1 * mm, fill=1, stroke=0)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 28)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.62, "BJP TECHNOLOGIES")
    canvas.setFont("Helvetica", 16)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.62 - 12 * mm, "(T) LIMITED")

    canvas.setFillColor(CYAN)
    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.45, "SESSION 14")
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.45 - 9 * mm, "GOOGLE ANALYTICS 4 INTEGRATION")

    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.30, "Date: 27 May 2026")
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.30 - 6 * mm, "Project: bjptechnologies.co.tz")
    canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.30 - 12 * mm, "Phase 6 — Polish & Launch")

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W / 2, 20 * mm, "Secure Technology. Scalable Growth.")
    canvas.restoreState()


def build_styles():
    return {
        "section": ParagraphStyle(
            "section",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=NAVY,
            spaceBefore=8 * mm,
            spaceAfter=3 * mm,
        ),
        "subsection": ParagraphStyle(
            "subsection",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=BLUE,
            spaceBefore=4 * mm,
            spaceAfter=2 * mm,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=BLACK,
            leading=14,
            spaceAfter=3 * mm,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=BLACK,
            leading=14,
            leftIndent=10 * mm,
            spaceAfter=1.5 * mm,
        ),
        "code": ParagraphStyle(
            "code",
            fontName="Courier",
            fontSize=8.5,
            textColor=BLUE,
            leading=13,
            leftIndent=6 * mm,
            spaceAfter=2 * mm,
            backColor=OFF_WHITE,
        ),
        "label": ParagraphStyle(
            "label",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=NAVY,
        ),
        "tag": ParagraphStyle(
            "tag",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=BLUE,
        ),
    }


def ruled_table(data, col_widths, header_bg=NAVY, header_fg=WHITE):
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), header_bg),
            ("TEXTCOLOR", (0, 0), (-1, 0), header_fg),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
            ("GRID", (0, 0), (-1, -1), 0.4, GREY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
    )
    return Table(data, colWidths=col_widths, style=style, repeatRows=1)


def build_story(styles):
    s = styles
    story = []

    # ── Overview ─────────────────────────────────────────────────────────────
    story.append(Paragraph("1. Overview", s["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=CYAN, spaceAfter=3 * mm))
    story.append(
        Paragraph(
            "This session integrated <b>Google Analytics 4 (GA4)</b> into the BJP Technologies "
            "website end to end, following the GA4 Integration Playbook. The work shipped in two "
            "independent phases: a client-side tracking tag that collects visitor data, and an "
            "in-admin dashboard that reads that data back through the GA4 Data API and renders it "
            "natively inside the Django admin.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "Two GA4 identifiers are used and must never be confused: the <b>Measurement ID</b> "
            "(<font name='Courier'>G-C9L66H4VE4</font>) drives the client-side tag, while the "
            "numeric <b>Property ID</b> (<font name='Courier'>538536674</font>) is used by the "
            "server-side Data API for the dashboard.",
            s["body"],
        )
    )

    # ── Phase 1 ──────────────────────────────────────────────────────────────
    story.append(Paragraph("2. Phase 1 — The Tracking Tag", s["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=CYAN, spaceAfter=3 * mm))
    story.append(
        Paragraph(
            "The gtag.js tag is injected on every public page and is fully controllable from the "
            "admin. It is emitted only when it is safe and wanted — never in local development.",
            s["body"],
        )
    )
    p1 = [
        ["Component", "Behaviour"],
        ["Measurement ID storage", "Editable in admin via SiteSettings; seeded on first deploy"],
        ["Master kill switch", "ga_enabled toggle disables tracking site-wide"],
        ["DEBUG suppression", "Tag never renders while DEBUG=True (no polluting prod stats)"],
        ["Conversion event", "contact_submit fires on the contact success page"],
        ["Admin entry", "Analytics > Google Analytics (editable Measurement ID + switch)"],
    ]
    story.append(ruled_table(p1, [48 * mm, CONTENT_W - 48 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(
        Paragraph(
            "<b>Emit condition:</b> "
            "<font name='Courier'>not DEBUG and ga_enabled and bool(ga_measurement_id)</font>",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Status:</b> Merged to develop via PR #62. Verified live in GA4 Realtime.",
            s["body"],
        )
    )

    # ── Phase 2 ──────────────────────────────────────────────────────────────
    story.append(Paragraph("3. Phase 2 — The In-Admin Dashboard", s["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=CYAN, spaceAfter=3 * mm))
    story.append(
        Paragraph(
            "A new <font name='Courier'>apps/analytics</font> app surfaces GA4 traffic directly "
            "inside the Unfold admin — same sidebar, breadcrumbs, and dark mode as the rest of the "
            "panel. All Data API calls pass through one cached gateway to stay within the "
            "~25,000 token/day quota.",
            s["body"],
        )
    )
    p2 = [
        ["Dashboard Card", "Data Shown", "Cache TTL"],
        ["Realtime active users", "Users on the site right now", "60s"],
        ["Traffic KPIs", "Users + page views (today / 7d / 30d)", "30 min"],
        ["Top pages", "Most-viewed pages (7 days)", "1 hr"],
        ["Traffic sources", "Where visitors came from (7 days)", "1 hr"],
        ["Top countries", "Visitor countries (30 days)", "1 hr"],
        ["Device split", "Mobile / desktop / tablet (30 days)", "1 hr"],
        ["Conversions", "contact_submit count (30 days)", "30 min"],
    ]
    story.append(ruled_table(p2, [42 * mm, CONTENT_W - 42 * mm - 22 * mm, 22 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(
        Paragraph(
            "<b>Authentication:</b> OAuth user-token (the GA4-admin account), not a service "
            "account — GA4 will not attach a service account to a property owned by a personal "
            "Gmail. A refresh token was captured once via the "
            "<font name='Courier'>ga_capture_token</font> command and stored in environment "
            "variables; <font name='Courier'>ga_verify</font> confirmed it works.",
            s["body"],
        )
    )

    # ── Technical traps handled ──────────────────────────────────────────────
    story.append(Paragraph("4. Technical Traps Handled", s["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=CYAN, spaceAfter=3 * mm))
    traps = [
        ["Trap", "Resolution"],
        [
            "Measurement ID vs Property ID confusion",
            "Documented and separated: tag uses G-, Data API uses the numeric ID",
        ],
        [
            "Every KPI shows 0 (reading totals[])",
            "Read headline numbers from rows[0]; totals[] is empty without aggregations",
        ],
        [
            "Unfold's narrow Tailwind bundle drops utility classes",
            "Dashboard ships its own scoped .ga-dash raw CSS instead of utilities",
        ],
        [
            "Dashboard page rendered with no admin chrome",
            "Virtual model + changelist_view merging admin_site.each_context()",
        ],
        [
            "OAuth refresh token expires after 7 days",
            "Consent screen published to 'In production' (not Testing)",
        ],
    ]
    story.append(ruled_table(traps, [70 * mm, CONTENT_W - 70 * mm]))

    # ── Repo-specific adaptations ────────────────────────────────────────────
    story.append(Paragraph("5. Adaptations to This Codebase", s["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=CYAN, spaceAfter=3 * mm))
    adapt = [
        ["Playbook assumed", "This repo uses", "Adaptation"],
        ["UUID singleton PK", "Integer pk=1", "Seed migration targets pk=1"],
        ["django-environ env()", "python-dotenv + os.environ", "os.environ.get(...)"],
        ["Inline success render", "FormView -> redirect", "Event fired on success view"],
        ["Many conversion events", "One contact form", "Single event: contact_submit"],
    ]
    story.append(ruled_table(adapt, [42 * mm, 44 * mm, CONTENT_W - 42 * mm - 44 * mm]))

    # ── Quality ──────────────────────────────────────────────────────────────
    story.append(Paragraph("6. Quality &amp; Verification", s["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=CYAN, spaceAfter=3 * mm))
    for item in [
        "<b>86 / 86</b> tests passing (19 new: 6 Phase 1, 13 Phase 2)",
        "ruff and black clean on all new files",
        "Live API confirmed: ga_verify returns 'Auth works'; dashboard context builds with no errors",
        "Dashboard rendered and screenshotted in admin — chrome intact, brand gradients applied",
    ]:
        story.append(Paragraph(f"&#8226; &nbsp; {item}", s["bullet"]))

    # ── Current state ────────────────────────────────────────────────────────
    story.append(Paragraph("7. Current State &amp; Next Steps", s["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=CYAN, spaceAfter=3 * mm))
    state = [
        ["Item", "Status", "Notes"],
        ["Phase 1 — tracking tag", "Complete", "Merged to develop (PR #62), live"],
        ["Phase 2 — dashboard", "Complete (code)", "Branch pushed; pending deploy"],
        ["Server GA_* env vars", "Pending", "Add 4 vars in cPanel Python App"],
        ["Dashboard data", "Awaiting data", "Zeros until ~48h of collection"],
        ["GA4 Key Event", "Pending", "Mark contact_submit as Key Event"],
        ["OAuth 'In production'", "To confirm", "Prevents 7-day token expiry"],
    ]
    story.append(ruled_table(state, [52 * mm, 30 * mm, CONTENT_W - 52 * mm - 30 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(
        Paragraph(
            "<b>Why the dashboard currently shows zeros:</b> GA4 standard reports (users, page "
            "views, top pages, etc.) lag <b>24&ndash;48 hours</b> on a freshly created property — "
            "this is normal Google processing latency, not a fault. Authentication is confirmed "
            "working. Realtime confirms data arrival immediately; the historical cards will "
            "populate automatically as data accumulates.",
            s["body"],
        )
    )

    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.5, color=GREY, spaceAfter=3 * mm))
    story.append(
        Paragraph(
            "<i>Report prepared by Claude Code (Opus 4.7) — BJP Technologies (T) Limited "
            "— bjptechnologies.co.tz</i>",
            ParagraphStyle("footer_note", fontName="Helvetica-Oblique", fontSize=8, textColor=GREY),
        )
    )

    return story


def main():
    doc = BaseDocTemplate(OUTPUT, pagesize=A4)

    cover_frame = Frame(
        0,
        0,
        PAGE_W,
        PAGE_H,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="cover",
    )
    content_frame = Frame(18 * mm, 20 * mm, CONTENT_W, PAGE_H - 45 * mm, id="content")

    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page),
            PageTemplate(id="content", frames=[content_frame], onPage=header_footer),
        ]
    )

    styles = build_styles()
    story = [NextPageTemplate("content"), PageBreak()]
    story += build_story(styles)

    doc.build(story)
    print(f"PDF saved: {OUTPUT}")


if __name__ == "__main__":
    main()
