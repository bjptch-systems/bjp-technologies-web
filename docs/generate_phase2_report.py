"""Generate BJP Technologies Phase 2 Completion Report PDF."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = "docs/BJP_Technologies_Phase2_Report.pdf"

# ── Brand colours ──────────────────────────────────────────────────────────────
NAVY = colors.HexColor("#0D1B4B")
CYAN = colors.HexColor("#00C6FF")
GREY = colors.HexColor("#8A94B0")
OFF_WHITE = colors.HexColor("#F4F6FC")
GREEN = colors.HexColor("#2ECC71")
WHITE = colors.white
BLACK = colors.black
LIGHT_GREY = colors.HexColor("#E8ECF4")

PAGE_W, PAGE_H = A4


# ── Header / Footer ────────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    # Top navy bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 18 * mm, PAGE_W, 18 * mm, fill=1, stroke=0)
    # Left label
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(15 * mm, PAGE_H - 11 * mm, "BJP Technologies (T) Limited")
    # Right label in cyan
    canvas.setFillColor(CYAN)
    canvas.setFont("Helvetica", 9)
    label = "Phase 2 Completion Report — April 2026"
    canvas.drawRightString(PAGE_W - 15 * mm, PAGE_H - 11 * mm, label)
    # Cyan accent line
    canvas.setFillColor(CYAN)
    canvas.rect(0, PAGE_H - 19.5 * mm, PAGE_W, 1.5 * mm, fill=1, stroke=0)

    # Bottom cyan bar
    canvas.setFillColor(CYAN)
    canvas.rect(0, 0, PAGE_W, 8 * mm, fill=1, stroke=0)
    # Footer text
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(15 * mm, 2.8 * mm, "CONFIDENTIAL — For Internal Use Only")
    canvas.drawCentredString(PAGE_W / 2, 2.8 * mm, "bjptechnologies.co.tz")
    canvas.drawRightString(PAGE_W - 15 * mm, 2.8 * mm, f"Page {doc.page}")
    canvas.restoreState()


# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "CompanyTitle",
    fontName="Helvetica-Bold",
    fontSize=26,
    textColor=NAVY,
    spaceAfter=6,
    alignment=1,
)
tagline_style = ParagraphStyle(
    "Tagline",
    fontName="Helvetica",
    fontSize=12,
    textColor=GREY,
    spaceAfter=0,
    alignment=1,
)
section_style = ParagraphStyle(
    "Section",
    fontName="Helvetica-Bold",
    fontSize=14,
    textColor=CYAN,
    spaceBefore=14,
    spaceAfter=6,
)
subsection_style = ParagraphStyle(
    "SubSection",
    fontName="Helvetica-Bold",
    fontSize=11,
    textColor=NAVY,
    spaceBefore=10,
    spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body",
    fontName="Helvetica",
    fontSize=9.5,
    textColor=BLACK,
    leading=14,
    spaceAfter=6,
)
bold_body = ParagraphStyle(
    "BoldBody",
    fontName="Helvetica-Bold",
    fontSize=9.5,
    textColor=BLACK,
    leading=14,
)


# ── Table helpers ──────────────────────────────────────────────────────────────
def info_table(rows):
    t = Table(rows, colWidths=[50 * mm, 120 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), OFF_WHITE),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("ROWBACKGROUND", (0, 0), (-1, -1), [WHITE, OFF_WHITE]),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def milestone_table(rows):
    header = [
        Paragraph(
            "<b>Milestone</b>",
            ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
        ),
        Paragraph(
            "<b>Status</b>",
            ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
        ),
    ]
    data = [header] + rows
    t = Table(data, colWidths=[110 * mm, 60 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUND", (0, 1), (-1, -1), [WHITE, OFF_WHITE]),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def deliverable_table(rows, col_widths=None):
    if col_widths is None:
        col_widths = [8 * mm, 82 * mm, 80 * mm]
    header = [
        "",
        Paragraph(
            "<b>Deliverable</b>",
            ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
        ),
        Paragraph(
            "<b>Notes</b>",
            ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
        ),
    ]
    data = [header] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUND", (0, 1), (-1, -1), [WHITE, OFF_WHITE]),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TEXTCOLOR", (0, 1), (0, -1), GREEN),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ]
        )
    )
    return t


def check(text):
    return ["✓", text, ""]


def check2(text, note):
    return ["✓", text, note]


def status_ok(text):
    return [
        Paragraph(text, ParagraphStyle("ms", fontName="Helvetica", fontSize=9, textColor=BLACK)),
        Paragraph(
            "✓  Complete",
            ParagraphStyle("ok", fontName="Helvetica-Bold", fontSize=9, textColor=GREEN),
        ),
    ]


def status_partial(text, note):
    return [
        Paragraph(text, ParagraphStyle("ms", fontName="Helvetica", fontSize=9, textColor=BLACK)),
        Paragraph(
            f"✓  {note}",
            ParagraphStyle("pt", fontName="Helvetica-Bold", fontSize=9, textColor=CYAN),
        ),
    ]


# ── Document ───────────────────────────────────────────────────────────────────
def build():
    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=25 * mm,
        bottomMargin=18 * mm,
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="main",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=header_footer)])

    story = []

    # ── Cover page ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20 * mm))

    # Company name box
    cover_box = Table(
        [
            [Paragraph("BJP TECHNOLOGIES (T) LIMITED", title_style)],
            [Paragraph("Secure Technology. Scalable Growth.", tagline_style)],
        ],
        colWidths=[170 * mm],
    )
    cover_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), OFF_WHITE),
                ("BOX", (0, 0), (-1, -1), 1.5, CYAN),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(cover_box)
    story.append(Spacer(1, 10 * mm))

    # Report title box
    title_box = Table(
        [
            [
                Paragraph(
                    "CORE FOUNDATION COMPLETION REPORT",
                    ParagraphStyle(
                        "rt", fontName="Helvetica-Bold", fontSize=16, textColor=WHITE, alignment=1
                    ),
                )
            ]
        ],
        colWidths=[170 * mm],
    )
    title_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story.append(title_box)
    story.append(Spacer(1, 8 * mm))

    # Phase status
    phase_box = Table(
        [
            [
                Paragraph(
                    "PHASE 2 — COMPLETE",
                    ParagraphStyle(
                        "ph", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, alignment=1
                    ),
                )
            ]
        ],
        colWidths=[170 * mm],
    )
    phase_box.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (-1, -1), 2, CYAN),
                ("LINEABOVE", (0, 0), (-1, -1), 2, CYAN),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(phase_box)
    story.append(Spacer(1, 10 * mm))

    # Cover info table
    story.append(
        info_table(
            [
                ["Project", "Corporate Website & Service Platform"],
                ["Company", "BJP Technologies (T) Limited"],
                ["Primary Domain", "bjptechnologies.co.tz"],
                ["Report Date", "April 2026"],
                ["Prepared By", "Development Team"],
                ["Classification", "Confidential — Internal Use Only"],
            ]
        )
    )
    story.append(Spacer(1, 12 * mm))

    story.append(
        Paragraph(
            "This document confirms the successful completion of Phase 2 (Core Foundation) of the BJP "
            "Technologies corporate website project. All base templates, BJP brand design system, "
            "home page content sections, static assets, and CI/CD smoke tests have been built, "
            "reviewed, and deployed to https://bjptechnologies.co.tz.",
            ParagraphStyle(
                "intro",
                fontName="Helvetica",
                fontSize=9.5,
                textColor=NAVY,
                leading=15,
                alignment=1,
                spaceAfter=6,
            ),
        )
    )

    # ── Section 1: Executive Summary ───────────────────────────────────────────
    story.append(Paragraph("1. Executive Summary", section_style))
    story.append(
        Paragraph(
            "Phase 2 of the BJP Technologies (T) Limited corporate website is <b>complete</b>. "
            "The Django application at <b>https://bjptechnologies.co.tz</b> now renders a fully "
            "styled, professional home page using the Luminos template system adapted with BJP brand "
            "identity. All shared layout components (navbar, footer, base template), the BJP brand "
            "CSS layer, and seven home page content sections are live and functional.",
            body_style,
        )
    )

    story.append(
        milestone_table(
            [
                status_ok("Base templates created (base.html, navbar.html, footer.html)"),
                status_ok("BJP brand CSS layer (bjp.css) — additive overrides only"),
                status_ok("BJP logo pack integrated (navbar, footer, favicon, OG image)"),
                status_ok("Home page — 7 content sections built and deployed"),
                status_ok("Animated stat counters working (CounterUp.js)"),
                status_ok("All static assets copied and served via WhiteNoise (310 files)"),
                status_ok("Google Fonts loaded — DM Serif Display, Outfit, Space Mono"),
                status_ok("Mobile sidebar with BJP mark logo"),
                status_ok("Smoke tests added — CI pipeline passing (exit code 0)"),
                status_partial("Luminos template folder removed from repo", "Cleanup complete"),
            ]
        )
    )

    # ── Section 2: Project Overview ────────────────────────────────────────────
    story.append(Paragraph("2. Project Overview", section_style))
    story.append(
        info_table(
            [
                ["Company", "BJP Technologies (T) Limited"],
                ["Location", "Ubungo – Dar es Salaam, Tanzania"],
                ["Primary Domain", "bjptechnologies.co.tz"],
                ["Alias Domain", "technologies.bejundas.co.tz  (301 redirect — separate cPanel)"],
                ["Project Type", "Corporate Website & Service Platform"],
                ["Framework", "Django 6.0.4"],
                ["Python Version", "3.12.12"],
                ["Database", "MySQL 8.0.45 — bjptechn_bjp_db"],
                ["Application Server", "Phusion Passenger (WSGI) — cPanel shared hosting"],
                ["Server Host", "Shared hosting — simba server, IP 50.6.6.46"],
                ["Static Files", "WhiteNoise — CompressedManifestStaticFilesStorage"],
                ["CSS Framework", "Bootstrap 5 + Luminos template + bjp.css brand layer"],
                ["Version Control", "GitHub — MussaJabir/bjp-technologies-web (private)"],
                ["Active Branch", "develop (feature/phase-2-core-foundation merged)"],
                ["CI/CD", "GitHub Actions — deploy.yml"],
                ["Contact", "info@bjptechnologies.co.tz  |  +255 678 290 994"],
            ]
        )
    )

    # ── Section 3: Deliverables ────────────────────────────────────────────────
    story.append(Paragraph("3. Deliverables Completed", section_style))

    # 3.1 Base Templates
    story.append(Paragraph("3.1 Base Templates & Layout", subsection_style))
    story.append(
        deliverable_table(
            [
                check2(
                    "apps/core/templates/core/base.html",
                    "Full page shell — all blocks, Google Fonts, JS deferred, preloader, scroll-to-top",
                ),
                check2(
                    "apps/core/templates/core/navbar.html",
                    "header-area-four sticky structure, BJP logo, 7-service dropdown, hamburger",
                ),
                check2(
                    "apps/core/templates/core/footer.html",
                    "Luminos light gradient footer, CTA banner in BJP navy, contact links, social icons",
                ),
                check2("templates/404.html", "Custom 404 error page extending base.html"),
                check2("templates/500.html", "Custom 500 error page extending base.html"),
                check2(
                    "apps/main/templates/main/about.html", "Stub About page (full content Phase 3)"
                ),
            ]
        )
    )

    # 3.2 Brand & Design
    story.append(Paragraph("3.2 BJP Brand & Design System", subsection_style))
    story.append(
        deliverable_table(
            [
                check2(
                    "static/css/bjp.css",
                    "Purely additive — logo sizing, sticky nav navy, CTA navy, primary button navy, scroll progress cyan",
                ),
                check2(
                    "Navbar logo",
                    "bjp-logo-horizontal-light.png — cream on transparent, visible on dark navy background",
                ),
                check2(
                    "Footer logo",
                    "bjp-logo-horizontal-transparent.png — navy on transparent, visible on light footer background",
                ),
                check2("Favicon 32px", "bjp-favicon-32.png — browser tab icon"),
                check2(
                    "Favicon 64px", "bjp-favicon-64.png — sharper icon for browsers preferring 64px"
                ),
                check2("Apple touch icon", "bjp-favicon-256.png — iOS home screen icon"),
                check2(
                    "Open Graph image",
                    "bjp-app-icon-512-navy.png — social sharing preview (WhatsApp, LinkedIn)",
                ),
                check2(
                    "Mobile sidebar mark",
                    "bjp-mark-transparent.png — standalone BJP mark at top of mobile nav",
                ),
                check2(
                    "Google Fonts",
                    "DM Serif Display (headings), Outfit (body), Space Mono (labels)",
                ),
            ]
        )
    )

    # 3.3 Home Page Sections
    story.append(Paragraph("3.3 Home Page Content Sections", subsection_style))
    story.append(
        deliverable_table(
            [
                check2(
                    "Hero banner",
                    "Jarallax parallax background (banner-four-bg), BJP headline, dual CTA buttons",
                ),
                check2(
                    "3 top service cards",
                    "Software Development, Cloud & Infrastructure, Cybersecurity — single-service-area-4",
                ),
                check2(
                    "7-service grid",
                    "All BJP services with icon SVGs and links to service detail pages",
                ),
                check2(
                    "Animated stats",
                    "CounterUp.js — 7 Service Lines, 6 Industries, 24/7 Support, 100% Dedicated",
                ),
                check2(
                    "About strip",
                    "2-col: about/01.webp image + company intro, 4 trust points, CTA to About page",
                ),
                check2(
                    "Why Choose BJP",
                    "4 differentiator cards (single-working-process-choose-us) with tag badges",
                ),
                check2(
                    "Technology partners",
                    "FA6 brand icons: AWS, Azure, Python, Laravel, Linux, Ubuntu, Stripe + M-Pesa badge",
                ),
                check2(
                    "Industries section",
                    "6 industry cards from context (default_industries fallback)",
                ),
            ]
        )
    )

    # 3.4 Static Assets
    story.append(Paragraph("3.4 Static Assets", subsection_style))
    story.append(
        deliverable_table(
            [
                check2(
                    "static/css/style.css",
                    "Luminos base CSS (20,139 lines) — all original variables preserved",
                ),
                check2(
                    "static/css/plugins/",
                    "fontawesome.css, swiper.css, metismenu.css, magnifying-popup.css",
                ),
                check2("static/css/vendor/", "bootstrap.min.css"),
                check2(
                    "static/fonts/",
                    "FontAwesome 6 (brands, solid, regular, light, duotone)",
                ),
                check2(
                    "static/js/plugins/",
                    "jquery.js, counter-up.js, swiper.js, metismenu.js, svg-inject.js, smooth-scroll.js, popup.js",
                ),
                check2(
                    "static/js/vendor/",
                    "bootstrap.min.js, jarallax.js, waw.js (WOW.js), waypoint.js, contact-form.js",
                ),
                check2(
                    "static/js/main.js",
                    "Luminos main JS — navbar sticky, mobile menu, scroll-to-top, animations",
                ),
                check2(
                    "static/images/",
                    "All Luminos image assets — about, banner, brand, service icons, team, testimonials, etc.",
                ),
                check2(
                    "static/images/logo/",
                    "7 BJP logo variants — navbar, footer, favicons (32/64/256), OG image, mark",
                ),
                check2(
                    "collectstatic", "310 files collected to public/static/ on production server"
                ),
            ]
        )
    )

    # 3.5 Testing & CI
    story.append(Paragraph("3.5 Testing & CI/CD", subsection_style))
    story.append(
        deliverable_table(
            [
                check2(
                    "apps/main/tests/test_views.py",
                    "2 smoke tests: home page 200 OK, about page 200 OK",
                ),
                check2(
                    "CI pipeline fix",
                    "Fixed exit code 5 (no tests collected) — pytest now collects and passes 2 tests",
                ),
                check2("ruff check", "0 errors across all Python files"),
                check2("black --check", "50 files unchanged — formatting consistent"),
                check2("python manage.py check", "0 issues on system check"),
                check2("GitHub Actions", "CI pipeline passing green on develop branch"),
            ]
        )
    )

    # ── Section 4: Technical Architecture ─────────────────────────────────────
    story.append(Paragraph("4. Frontend Technical Architecture", section_style))

    arch_data = [
        [
            Paragraph(
                "<b>Layer</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>Technology</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>Notes</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
        ],
        ["Template Engine", "Django Templates", "Jinja2 not used — pure Django blocks and tags"],
        [
            "Base Layout",
            "Luminos index-four.html",
            "header-area-four design — transparent nav over dark hero",
        ],
        [
            "CSS Base",
            "style.css (Luminos)",
            "All original variables preserved — no internal overrides",
        ],
        ["CSS Brand Layer", "bjp.css", "Purely additive — 47 lines, BJP navy/cyan identity only"],
        ["CSS Framework", "Bootstrap 5", "Grid, utilities, responsive breakpoints"],
        [
            "Icons",
            "FontAwesome 6 Pro",
            "Solid, regular, light, duotone, brands — local files (no CDN)",
        ],
        [
            "Fonts",
            "Google Fonts",
            "Loaded in base.html head — DM Serif Display, Outfit, Space Mono",
        ],
        [
            "Animations",
            "WOW.js + Animate.css",
            "Scroll-reveal — fadeInUp, fadeInLeft, fadeInRight classes",
        ],
        ["Parallax", "Jarallax", "Hero section background — data-speed='0.5'"],
        ["Counters", "CounterUp.js + Waypoint", ".counter span triggers on scroll into viewport"],
        ["Slider", "Swiper.js", "Available for Phase 3 testimonials / case studies"],
        [
            "Static Serving",
            "WhiteNoise",
            "CompressedManifestStaticFilesStorage — gzip + cache fingerprinting",
        ],
        ["Mobile Nav", "MetisMenu.js", "Collapsible sidebar with BJP mark logo at top"],
    ]

    arch_t = Table(arch_data, colWidths=[38 * mm, 42 * mm, 90 * mm])
    arch_t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUND", (0, 1), (-1, -1), [WHITE, OFF_WHITE]),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TEXTCOLOR", (0, 1), (-1, -1), BLACK),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 1), (0, -1), NAVY),
            ]
        )
    )
    story.append(arch_t)

    # ── Section 5: Home Page Structure ────────────────────────────────────────
    story.append(Paragraph("5. Home Page Section Map", section_style))

    hp_data = [
        [
            Paragraph(
                "<b>#</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>Section</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>CSS Class / Plugin</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>Content</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
        ],
        [
            "1",
            "Hero Banner",
            "banner-four-area banner-four-bg / Jarallax",
            "Headline, tagline, 2 CTA buttons",
        ],
        [
            "2",
            "Top 3 Service Cards",
            "service-area-start / single-service-area-4",
            "Software Dev, Cloud, Cybersecurity",
        ],
        [
            "3",
            "All 7 Services Grid",
            "innovative-solution / single-service-area-wrapper",
            "Full service catalogue with icons",
        ],
        [
            "4",
            "Animated Stats",
            "counter-up-wrapper / CounterUp.js",
            "7 Services, 6 Industries, 24/7, 100%",
        ],
        ["5", "About Strip", "what-we-do-main-wrapper", "Image + trust points + CTA to About"],
        [
            "6",
            "Why Choose BJP",
            "single-working-process-choose-us",
            "4 differentiator cards with tag badges",
        ],
        [
            "7",
            "Tech Partners",
            "brand-area-main-wrapper / FA6 icons",
            "AWS, Azure, Python, Laravel, Linux, M-Pesa",
        ],
        ["8", "Industries", "single-service-area-wrapper", "6 industry sector cards"],
    ]

    hp_t = Table(hp_data, colWidths=[8 * mm, 42 * mm, 58 * mm, 62 * mm])
    hp_t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUND", (0, 1), (-1, -1), [WHITE, OFF_WHITE]),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TEXTCOLOR", (0, 1), (-1, -1), BLACK),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 1), (0, -1), NAVY),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ]
        )
    )
    story.append(hp_t)

    # ── Section 6: Known Limitations ──────────────────────────────────────────
    story.append(Paragraph("6. Known Limitations / Pending Items", section_style))

    lim_data = [
        [
            Paragraph(
                "<b>Item</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>Detail</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>Resolution</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
        ],
        [
            "SSH auto-deploy blocked",
            "Port 22 blocked on shared hosting — GitHub Actions deploy step inactive",
            "Manual pull via cPanel Git Version Control (interim)",
        ],
        [
            "About page — stub only",
            "about.html contains placeholder text, not full content",
            "Full About page built in Phase 3",
        ],
        [
            "Service / Industry pages — stubs",
            "Services and Industries return empty stub templates",
            "Models + full templates built in Phase 3",
        ],
        [
            "About strip image — placeholder",
            "Uses Luminos about/01.webp, not real BJP photography",
            "Replace with real photo in Phase 5/6",
        ],
        [
            "Tech partner logos — icon-based",
            "FA6 brand icons used; no official partner SVG logos available",
            "Replace with official logos in Phase 6 if obtained",
        ],
        [
            "collectstatic — manual step",
            "Must be run manually in cPanel after each deploy",
            "Will be automated once SSH access is resolved",
        ],
    ]

    lim_t = Table(lim_data, colWidths=[42 * mm, 72 * mm, 56 * mm])
    lim_t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUND", (0, 1), (-1, -1), [WHITE, OFF_WHITE]),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TEXTCOLOR", (0, 1), (-1, -1), BLACK),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 1), (0, -1), NAVY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(lim_t)

    # ── Section 7: Phase 3 Next Steps ─────────────────────────────────────────
    story.append(Paragraph("7. Phase 3 — Content Pages (Next)", section_style))
    story.append(
        Paragraph(
            "Phase 3 will build all public-facing content pages, connect them to database models, "
            "and seed the 7 services and 6 industries into the MySQL database.",
            body_style,
        )
    )

    next_data = [
        [
            Paragraph(
                "<b>Deliverable</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
            Paragraph(
                "<b>Scope</b>",
                ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE),
            ),
        ],
        ["apps/main/ — About page", "Full About page: company story, team, values, stats"],
        [
            "apps/services/ — Service model",
            "Django model: name, slug, description, icon, order, is_active",
        ],
        [
            "apps/services/ — Services list",
            "All 7 services listed with icons and brief descriptions",
        ],
        ["apps/services/ — Service detail", "Individual service page with full content and CTA"],
        ["apps/industries/ — Industry model", "Django model: name, slug, description, is_active"],
        ["apps/industries/ — Industries list", "All 6 industries with descriptions"],
        ["apps/industries/ — Industry detail", "Individual industry page with relevant services"],
        ["Data seeding", "Management command or fixture to seed 7 services + 6 industries"],
        ["Mobile responsiveness", "All pages verified at 375px, 768px, 1024px, 1440px"],
        ["Tests", "Views, models, and URL tests for all new pages"],
    ]

    next_t = Table(next_data, colWidths=[75 * mm, 95 * mm])
    next_t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUND", (0, 1), (-1, -1), [WHITE, OFF_WHITE]),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 1), (-1, -1), BLACK),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 1), (0, -1), NAVY),
            ]
        )
    )
    story.append(next_t)

    story.append(Spacer(1, 8 * mm))
    story.append(
        Paragraph(
            "Phase 3 will begin upon receipt of the Phase 2 go-ahead from the project owner.",
            ParagraphStyle(
                "note", fontName="Helvetica-Oblique", fontSize=9, textColor=GREY, alignment=1
            ),
        )
    )

    doc.build(story)
    print(f"Report generated: {OUTPUT}")


if __name__ == "__main__":
    build()
