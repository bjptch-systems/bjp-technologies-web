"""PDPC compliance — Privacy Policy page, cookie banner, footer links, address."""

from datetime import date

import pytest
from django.urls import reverse

from apps.core.models import SiteSettings

PRIVACY_URL = reverse("main:privacy")


@pytest.mark.django_db
def test_privacy_page_returns_200(client):
    response = client.get(PRIVACY_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_privacy_page_uses_correct_template(client):
    response = client.get(PRIVACY_URL)
    assert "main/privacy.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_privacy_page_shows_seeded_policy(client):
    html = client.get(PRIVACY_URL).content.decode()
    assert "Personal Data Protection Act of Tanzania" in html
    assert "privacy@bjptechnologies.co.tz" in html
    assert "Msakuzi, Ubungo, Dar es Salaam, 16113, Tanzania" in html


@pytest.mark.django_db
def test_privacy_page_reflects_admin_edits(client):
    site = SiteSettings.get()
    site.privacy_policy_body = "<p>Edited policy text</p>"
    site.privacy_policy_updated = date(2026, 11, 1)
    site.save()
    html = client.get(PRIVACY_URL).content.decode()
    assert "<p>Edited policy text</p>" in html
    assert "Last updated: 1 November 2026" in html


@pytest.mark.django_db
def test_privacy_page_in_sitemap(client):
    xml = client.get("/sitemap.xml").content.decode()
    assert "/privacy-policy/" in xml


@pytest.mark.django_db
def test_every_page_has_cookie_banner_and_footer_links(client):
    html = client.get(reverse("main:home")).content.decode()
    assert 'id="cookie-banner"' in html
    assert 'data-cookie-choice="accepted"' in html
    assert 'data-cookie-choice="rejected"' in html
    assert f'href="{PRIVACY_URL}"' in html
    assert "data-cookie-settings" in html


@pytest.mark.django_db
def test_footer_shows_new_address(client):
    html = client.get(reverse("main:home")).content.decode()
    assert "Msakuzi, Ubungo, Dar es Salaam, 16113, Tanzania" in html
