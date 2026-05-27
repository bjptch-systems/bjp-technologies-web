"""Phase 1 GA4 tracking — tag injection, kill-switch, and conversion events."""

import pytest
from django.test import override_settings
from django.urls import reverse

from apps.core.models import SiteSettings

HOME_URL = reverse("main:home")
SUCCESS_URL = reverse("contact:success")

# DEBUG=False is required for the tag to render at all; the test client uses the
# "testserver" host, which must be allowed once DEBUG is off.
PROD_LIKE = override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])


@pytest.fixture
def settings_with_ga(db):
    site = SiteSettings.get()
    site.ga_measurement_id = "G-C9L66H4VE4"
    site.ga_enabled = True
    site.save()
    return site


# --- The tag itself ---


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_tag_not_rendered_in_debug(client, settings_with_ga):
    """Local dev (DEBUG=True) must never emit the tag — no polluting prod stats.
    (pytest-django forces DEBUG=False during tests, so we override it back on here.)"""
    html = client.get(HOME_URL).content.decode()
    assert "googletagmanager.com/gtag/js" not in html
    assert "G-C9L66H4VE4" not in html


@pytest.mark.django_db
@PROD_LIKE
def test_tag_rendered_when_enabled(client, settings_with_ga):
    html = client.get(HOME_URL).content.decode()
    assert "googletagmanager.com/gtag/js?id=G-C9L66H4VE4" in html
    assert "gtag('config', 'G-C9L66H4VE4')" in html


@pytest.mark.django_db
@PROD_LIKE
def test_tag_suppressed_when_switch_off(client, settings_with_ga):
    settings_with_ga.ga_enabled = False
    settings_with_ga.save()
    html = client.get(HOME_URL).content.decode()
    assert "G-C9L66H4VE4" not in html


@pytest.mark.django_db
@PROD_LIKE
def test_tag_suppressed_when_id_blank(client, settings_with_ga):
    settings_with_ga.ga_measurement_id = ""
    settings_with_ga.save()
    html = client.get(HOME_URL).content.decode()
    assert "googletagmanager.com/gtag/js" not in html


# --- Conversion events ---


@pytest.mark.django_db
@PROD_LIKE
def test_conversion_event_fires_on_success_page(client, settings_with_ga):
    html = client.get(SUCCESS_URL).content.decode()
    assert "gtag('event', 'contact_submit'" in html


@pytest.mark.django_db
@PROD_LIKE
def test_no_conversion_event_on_normal_page(client, settings_with_ga):
    html = client.get(HOME_URL).content.decode()
    assert "gtag('event'" not in html
