import logging

from django.contrib import admin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from unfold.admin import ModelAdmin

from apps.analytics import services
from apps.analytics.models import AnalyticsOverview

logger = logging.getLogger(__name__)


def _build_dashboard_context() -> dict:
    """Call each service helper inside one try/except so a single failing report
    surfaces an error banner instead of a 500. Also computes max_* values for the
    bar widths. Kept module-level (not a method) so tests can call it with
    `services` mocked.
    """
    ctx: dict = {"error": None}
    try:
        kpis = services.headline_kpis()
        pages = services.top_pages(limit=5)
        sources = services.top_sources(limit=5)
        countries = services.top_countries(limit=5)
        devices = services.device_breakdown()
        conversions = services.conversions_30d()

        device_total = sum(d.value for d in devices)
        # kpis is a flat [users, views, users, views, ...] — pair into 3 cards.
        traffic_cards = [
            {"window": kpis[i].window, "users": kpis[i].value, "views": kpis[i + 1].value}
            for i in range(0, len(kpis), 2)
        ]
        ctx.update(
            {
                "realtime_users": services.realtime_active_users(),
                "kpis": kpis,
                "traffic_cards": traffic_cards,
                "top_pages": pages,
                "top_sources": sources,
                "top_countries": countries,
                "devices": devices,
                "conversions": conversions,
                "total_conversions": sum(c.count for c in conversions),
                # guard each max at >= 1 so widthratio never divides by zero
                "max_page_views": max((p.value for p in pages), default=1) or 1,
                "max_source_sessions": max((s.value for s in sources), default=1) or 1,
                "max_country_users": max((c.value for c in countries), default=1) or 1,
                "device_total": device_total or 1,
            }
        )
    except Exception as exc:  # noqa: BLE001 — surface any API error in the banner
        logger.exception("GA4 dashboard failed to build")
        ctx["error"] = str(exc)
    return ctx


@admin.register(AnalyticsOverview)
class AnalyticsOverviewAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return bool(request.user and request.user.is_staff)

    def changelist_view(self, request, extra_context=None):
        base_ctx = self.admin_site.each_context(request)  # ← the admin chrome

        if not services.is_configured():
            return TemplateResponse(
                request,
                "admin/analytics/not_configured.html",
                {**base_ctx, "title": "Analytics — Setup Required"},
            )

        if request.GET.get("refresh") == "1":
            services.invalidate_all()
            return redirect(request.path)

        ctx = _build_dashboard_context()
        ctx.update(base_ctx)
        ctx["title"] = "Analytics — Overview"
        if extra_context:
            ctx.update(extra_context)
        return TemplateResponse(request, "admin/analytics/overview.html", ctx)
