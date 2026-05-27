"""Admin/dashboard tests — `services` is mocked at its point of use."""

from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.analytics import services as real_services
from apps.analytics.admin import _build_dashboard_context

URL = reverse("admin:analytics_analyticsoverview_changelist")


def _fake_services():
    """A mock `services` module returning real typed rows so the template renders."""
    m = MagicMock()
    m.is_configured.return_value = True
    m.realtime_active_users.return_value = 5
    m.headline_kpis.return_value = [
        real_services.Kpi("Users (Today)", 3, "today"),
        real_services.Kpi("Page Views (Today)", 8, "today"),
        real_services.Kpi("Users (7d)", 30, "last 7 days"),
        real_services.Kpi("Page Views (7d)", 80, "last 7 days"),
        real_services.Kpi("Users (30d)", 120, "last 30 days"),
        real_services.Kpi("Page Views (30d)", 300, "last 30 days"),
    ]
    m.top_pages.return_value = [real_services.NamedRow("Home", 40, "/")]
    m.top_sources.return_value = [real_services.NamedRow("google", 22)]
    m.top_countries.return_value = [real_services.NamedRow("Tanzania", 90)]
    m.device_breakdown.return_value = [
        real_services.NamedRow("Mobile", 70),
        real_services.NamedRow("Desktop", 30),
    ]
    m.conversions_30d.return_value = [real_services.ConversionRow("contact_submit", 4)]
    return m


def test_build_dashboard_context_shape():
    with patch("apps.analytics.admin.services", _fake_services()):
        ctx = _build_dashboard_context()

    assert ctx["error"] is None
    assert ctx["realtime_users"] == 5
    assert ctx["total_conversions"] == 4
    # flat KPI list paired into 3 cards
    assert len(ctx["traffic_cards"]) == 3
    assert ctx["traffic_cards"][0] == {"window": "today", "users": 3, "views": 8}
    # max_* feed the bar widths and must never be zero
    assert ctx["max_page_views"] == 40
    assert ctx["device_total"] == 100


def test_build_dashboard_context_guards_against_empty():
    """No data anywhere → max_* stay >= 1 so widthratio never divides by zero."""
    empty = MagicMock()
    empty.is_configured.return_value = True
    empty.realtime_active_users.return_value = 0
    empty.headline_kpis.return_value = []
    empty.top_pages.return_value = []
    empty.top_sources.return_value = []
    empty.top_countries.return_value = []
    empty.device_breakdown.return_value = []
    empty.conversions_30d.return_value = []
    with patch("apps.analytics.admin.services", empty):
        ctx = _build_dashboard_context()
    assert ctx["max_page_views"] == 1
    assert ctx["device_total"] == 1
    assert ctx["traffic_cards"] == []


def test_build_dashboard_context_catches_api_error():
    boom = MagicMock()
    boom.is_configured.return_value = True
    boom.headline_kpis.side_effect = RuntimeError("token expired")
    with patch("apps.analytics.admin.services", boom):
        ctx = _build_dashboard_context()
    assert "token expired" in ctx["error"]


@pytest.mark.django_db
def test_overview_renders_with_admin_chrome(admin_client):
    """Regression for the missing-chrome bug: each_context() output must be merged,
    so available_apps (sidebar) and site_header are in the response context."""
    with patch("apps.analytics.admin.services", _fake_services()):
        resp = admin_client.get(URL)
    assert resp.status_code == 200
    assert "admin/analytics/overview.html" in [t.name for t in resp.templates]
    assert "available_apps" in resp.context
    assert "site_header" in resp.context


@pytest.mark.django_db
def test_overview_renders_with_empty_data(admin_client):
    """Today's real state: configured but property < 48h old, so every report is
    empty. The template must still render (no widthratio div-by-zero, no resetcycle
    error on an empty device loop)."""
    empty = MagicMock()
    empty.is_configured.return_value = True
    empty.realtime_active_users.return_value = 0
    empty.headline_kpis.return_value = []
    empty.top_pages.return_value = []
    empty.top_sources.return_value = []
    empty.top_countries.return_value = []
    empty.device_breakdown.return_value = []
    empty.conversions_30d.return_value = []
    with patch("apps.analytics.admin.services", empty):
        resp = admin_client.get(URL)
    assert resp.status_code == 200
    assert "admin/analytics/overview.html" in [t.name for t in resp.templates]


@pytest.mark.django_db
def test_not_configured_page(admin_client):
    not_cfg = MagicMock()
    not_cfg.is_configured.return_value = False
    with patch("apps.analytics.admin.services", not_cfg):
        resp = admin_client.get(URL)
    assert resp.status_code == 200
    assert "admin/analytics/not_configured.html" in [t.name for t in resp.templates]


@pytest.mark.django_db
def test_refresh_busts_cache_and_redirects(admin_client):
    fake = _fake_services()
    with patch("apps.analytics.admin.services", fake):
        resp = admin_client.get(URL + "?refresh=1")
    fake.invalidate_all.assert_called_once()
    assert resp.status_code == 302


@pytest.mark.django_db
def test_non_staff_denied(client):
    user = get_user_model().objects.create_user(
        username="visitor", password="pw12345", is_staff=False
    )
    client.force_login(user)
    resp = client.get(URL)
    assert resp.status_code in (302, 403)
