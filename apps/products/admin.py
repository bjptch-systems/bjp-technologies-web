from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin

from .models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        "name",
        "show_status",
        "show_tagline",
        "order",
        "show_contact_state",
        "show_link",
        "show_actions",
    ]
    list_display_links = ["name"]
    list_editable = ["order"]
    list_filter = ["status"]
    list_per_page = 25
    search_fields = ["name", "tagline", "short_description", "long_description"]
    prepopulated_fields = {"slug": ("name",)}
    save_as = True
    actions = ["mark_live", "mark_coming_soon"]

    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    ("name", "status"),
                    ("tagline", "order"),
                    "byline",
                    "live_url",
                ),
            },
        ),
        (
            "Descriptions",
            {
                "fields": ("short_description", "long_description"),
                "description": (
                    "Short description is used on the home-page card. "
                    "Long description is used on the detail page hero — line breaks become paragraphs."
                ),
            },
        ),
        (
            "Detail page sections",
            {
                "fields": (
                    "problem_statements",
                    "target_users",
                    "features",
                    "differentiators",
                    "how_it_works_steps",
                    "pricing_summary",
                    "onboarding_promise",
                    "disclosures",
                ),
                "description": (
                    "problem_statements / target_users / differentiators / how_it_works_steps "
                    "/ disclosures — one item per line. features — JSON list of "
                    '{"name", "description", "icon"} dicts. disclosures renders as a small '
                    "'Currently shipping' callout — leave blank to hide it."
                ),
            },
        ),
        (
            "Calls to action",
            {
                "fields": (
                    ("cta_primary_label", "cta_primary_url"),
                    ("cta_secondary_label", "cta_secondary_url"),
                ),
            },
        ),
        (
            "Contact block (optional)",
            {
                "fields": (
                    ("contact_email", "contact_phone"),
                    ("contact_hours", "contact_whatsapp"),
                ),
                "classes": ("collapse",),
                "description": (
                    "The contact block is hidden on the detail page until at least one field is "
                    "populated. Leave blank to omit the block entirely."
                ),
            },
        ),
        (
            "SEO",
            {
                "fields": ("meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            "Assets",
            {
                "fields": (
                    ("hero_image", "og_image"),
                    ("logo_image", "accent_color"),
                    "screenshots",
                ),
                "description": (
                    "Image fields hold relative paths under static/images/, "
                    "e.g. 'products/pms/hero-dashboard.png'. Copy the file into that location. "
                    "screenshots — JSON list of "
                    '{"image", "caption"} dicts for the gallery.'
                ),
            },
        ),
        (
            "Advanced",
            {
                "fields": ("slug", "created_at", "updated_at"),
                "classes": ("collapse",),
                "description": (
                    "Slug is auto-generated from the name on first save. "
                    "Only edit it if you have a specific reason."
                ),
            },
        ),
    )
    readonly_fields = ["created_at", "updated_at"]

    @admin.display(description="Status")
    def show_status(self, obj):
        color = "#16a34a" if obj.is_live else "#f59e0b"
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 10px; '
            "border-radius:999px; font-size:11px; font-weight:600; "
            'text-transform:uppercase;">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.display(description="Tagline")
    def show_tagline(self, obj):
        if not obj.tagline:
            return "—"
        return obj.tagline[:60] + ("…" if len(obj.tagline) > 60 else "")

    @admin.display(description="Contact")
    def show_contact_state(self, obj):
        # mark_safe — no user input to escape; format_html with zero args
        # raises TypeError on Django 6.
        if obj.has_contact_block:
            return mark_safe('<span style="color:#16a34a;">✓ filled</span>')
        return mark_safe('<span style="color:#9ca3af;">— empty</span>')

    @admin.display(description="Site")
    def show_link(self, obj):
        if not obj.is_live:
            return "—"
        return format_html(
            '<a href="/products/{}/" target="_blank" style="white-space:nowrap;">View →</a>',
            obj.slug,
        )

    @admin.display(description="Actions")
    def show_actions(self, obj):
        edit_url = reverse("admin:products_product_change", args=[obj.pk])
        delete_url = reverse("admin:products_product_delete", args=[obj.pk])
        return format_html(
            '<a href="{}" style="margin-right:8px; padding:3px 10px; border-radius:4px; '
            'background:#1565C0; color:#fff; font-size:12px; text-decoration:none;">Edit</a>'
            '<a href="{}" style="padding:3px 10px; border-radius:4px; '
            'background:#e53935; color:#fff; font-size:12px; text-decoration:none;">Delete</a>',
            edit_url,
            delete_url,
        )

    @admin.action(description="Mark selected products as Live")
    def mark_live(self, request, queryset):
        updated = queryset.update(status=Product.STATUS_LIVE)
        self.message_user(request, f"{updated} product(s) marked as live.")

    @admin.action(description="Mark selected products as Coming Soon")
    def mark_coming_soon(self, request, queryset):
        updated = queryset.update(status=Product.STATUS_COMING_SOON)
        self.message_user(request, f"{updated} product(s) marked as coming soon.")
