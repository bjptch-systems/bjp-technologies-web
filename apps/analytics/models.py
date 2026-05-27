from django.db import models


class AnalyticsOverview(models.Model):
    """Virtual entry point for the in-admin dashboard.

    The table is created empty and never written to — it exists only to give the
    admin a URL (changelist) to hand off to, so the dashboard can render *inside*
    the admin chrome (Unfold sidebar, breadcrumbs, dark mode) via each_context().
    """

    class Meta:
        verbose_name = "Overview"
        verbose_name_plural = "Overview"
        default_permissions = ()  # don't generate add/change/delete/view perms

    def __str__(self):  # pragma: no cover
        return "Analytics Overview"
