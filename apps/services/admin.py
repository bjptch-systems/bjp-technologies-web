from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Service


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = [
        "name",
        "show_tagline",
        "order",
        "show_active",
        "show_bullets",
        "show_link",
        "show_actions",
    ]
    list_display_links = ["name"]
    list_editable = ["order"]
    list_filter = ["is_active"]
    list_per_page = 25
    search_fields = ["name", "tagline", "description"]
    prepopulated_fields = {"slug": ("name",)}
    save_as = True
    actions = ["activate_services", "deactivate_services"]

    fieldsets = (
        (
            "Service Details",
            {
                "fields": (("name", "tagline"), ("order", "is_active")),
            },
        ),
        (
            "Content",
            {
                "fields": ("description", "bullet_points"),
                "description": "bullet_points — enter one item per line. Each line becomes a ✓ checkmark on the service detail page.",
            },
        ),
        (
            "Icon & Image",
            {
                "fields": ("icon_svg", "image"),
                "classes": ("collapse",),
            },
        ),
        (
            "Advanced",
            {
                "fields": ("slug", "created_at", "updated_at"),
                "classes": ("collapse",),
                "description": "Slug is auto-generated from the name on first save. Only edit it if you have a specific reason.",
            },
        ),
    )
    readonly_fields = ["created_at", "updated_at"]

    @admin.display(description="Tagline")
    def show_tagline(self, obj):
        if not obj.tagline:
            return "—"
        return obj.tagline[:65] + ("…" if len(obj.tagline) > 65 else "")

    @admin.display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active

    @admin.display(description="Bullets")
    def show_bullets(self, obj):
        count = len(obj.get_bullet_list())
        return f"{count} item{'s' if count != 1 else ''}"

    @admin.display(description="Site")
    def show_link(self, obj):
        return format_html(
            '<a href="/services/{}/" target="_blank" style="white-space:nowrap;">View →</a>',
            obj.slug,
        )

    @admin.display(description="Actions")
    def show_actions(self, obj):
        edit_url = reverse("admin:services_service_change", args=[obj.pk])
        delete_url = reverse("admin:services_service_delete", args=[obj.pk])
        return format_html(
            '<a href="{}" style="margin-right:8px; padding:3px 10px; border-radius:4px; '
            'background:#1565C0; color:#fff; font-size:12px; text-decoration:none;">Edit</a>'
            '<a href="{}" style="padding:3px 10px; border-radius:4px; '
            'background:#e53935; color:#fff; font-size:12px; text-decoration:none;">Delete</a>',
            edit_url,
            delete_url,
        )

    @admin.action(description="Activate selected services")
    def activate_services(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} service(s) marked as active.")

    @admin.action(description="Deactivate selected services")
    def deactivate_services(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} service(s) marked as inactive.")
