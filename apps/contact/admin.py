from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import ContactEnquiry


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(ModelAdmin):
    list_display = [
        "show_name",
        "email",
        "phone",
        "company",
        "service",
        "show_status",
        "created_at",
        "show_actions",
    ]
    list_display_links = ["show_name"]
    list_filter = ["status", "service", "created_at"]
    search_fields = ["first_name", "last_name", "email", "company", "message"]
    ordering = ["-created_at"]
    list_per_page = 25
    actions = ["mark_read", "mark_unread", "mark_replied"]

    # All client fields are readonly — only status is editable
    readonly_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "company",
        "service",
        "message",
        "ip_address",
        "consent_at",
        "privacy_policy_version",
        "created_at",
        "updated_at",
    ]

    fieldsets = [
        (
            "Client Details",
            {
                "fields": [
                    ("first_name", "last_name"),
                    ("email", "phone"),
                    "company",
                    "service",
                ],
            },
        ),
        (
            "Enquiry",
            {"fields": ["message"]},
        ),
        (
            "Status",
            {"fields": ["status"]},
        ),
        (
            "Privacy Consent",
            {"fields": [("consent_at", "privacy_policy_version")]},
        ),
        (
            "Meta",
            {
                "fields": ["ip_address", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Auto-mark enquiry as read when opened."""
        ContactEnquiry.objects.filter(pk=object_id, status=ContactEnquiry.STATUS_NEW).update(
            status=ContactEnquiry.STATUS_READ
        )
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.display(description="Name")
    def show_name(self, obj):
        return obj.full_name

    @admin.display(description="Status")
    def show_status(self, obj):
        colours = {
            ContactEnquiry.STATUS_NEW: ("#e53935", "#fff"),
            ContactEnquiry.STATUS_READ: ("#1565C0", "#fff"),
            ContactEnquiry.STATUS_REPLIED: ("#2e7d32", "#fff"),
        }
        bg, fg = colours.get(obj.status, ("#999", "#fff"))
        label = obj.get_status_display()
        return format_html(
            '<span style="padding:3px 10px; border-radius:4px; background:{}; '
            'color:{}; font-size:12px; font-weight:600;">{}</span>',
            bg,
            fg,
            label,
        )

    @admin.display(description="Actions")
    def show_actions(self, obj):
        edit_url = reverse("admin:contact_contactenquiry_change", args=[obj.pk])
        delete_url = reverse("admin:contact_contactenquiry_delete", args=[obj.pk])
        return format_html(
            '<a href="{}" style="margin-right:8px; padding:3px 10px; border-radius:4px; '
            'background:#1565C0; color:#fff; font-size:12px; text-decoration:none;">Open</a>'
            '<a href="{}" style="padding:3px 10px; border-radius:4px; '
            'background:#e53935; color:#fff; font-size:12px; text-decoration:none;">Delete</a>',
            edit_url,
            delete_url,
        )

    @admin.action(description="Mark selected as Read")
    def mark_read(self, request, queryset):
        updated = queryset.update(status=ContactEnquiry.STATUS_READ)
        self.message_user(request, f"{updated} enquiry/enquiries marked as read.")

    @admin.action(description="Mark selected as Unread")
    def mark_unread(self, request, queryset):
        updated = queryset.update(status=ContactEnquiry.STATUS_NEW)
        self.message_user(request, f"{updated} enquiry/enquiries marked as unread.")

    @admin.action(description="Mark selected as Replied")
    def mark_replied(self, request, queryset):
        updated = queryset.update(status=ContactEnquiry.STATUS_REPLIED)
        self.message_user(request, f"{updated} enquiry/enquiries marked as replied.")
