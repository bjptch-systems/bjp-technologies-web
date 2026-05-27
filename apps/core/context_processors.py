from django.conf import settings

from apps.industries.models import Industry
from apps.services.models import Service

from .models import SiteSettings


def company_info(request):
    site = SiteSettings.get()
    return {
        "company": site,
        "footer_services": Service.objects.filter(is_active=True).order_by("order"),
        "footer_industries": Industry.objects.filter(is_active=True).order_by("order"),
        # Only emit the GA4 tag when it's safe and wanted: never in local dev
        # (DEBUG), only when the master switch is on, and only if an ID exists.
        "analytics_enabled": (
            not settings.DEBUG and site.ga_enabled and bool(site.ga_measurement_id)
        ),
    }
