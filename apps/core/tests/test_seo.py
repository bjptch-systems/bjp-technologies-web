"""Release 1 (Nov 2026) — business details for Google, one canonical host, contact info."""

import json
import re

import pytest
from django.http import HttpResponse
from django.test import RequestFactory, override_settings
from django.urls import reverse

from apps.core.middleware import StripWwwMiddleware
from apps.core.models import SiteSettings

HOME_URL = reverse("main:home")
CONTACT_URL = reverse("contact:contact")


def jsonld(html: str) -> dict:
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert match, "no structured data on page"
    return json.loads(match.group(1))


@pytest.mark.django_db
@pytest.mark.parametrize("url", [HOME_URL, CONTACT_URL])
def test_business_details_match_google_profile(client, url):
    data = jsonld(client.get(url).content.decode())
    assert data["@type"] == "LocalBusiness"
    assert data["name"] == "BJP Technologies (T) Limited"
    assert data["telephone"] == "+255 764 764 011"
    assert data["address"]["streetAddress"] == "Msakuzi, Ubungo"
    assert data["address"]["postalCode"] == "16113"
    assert data["hasMap"] == "https://www.google.com/maps?cid=17710749172499910700"
    assert "https://www.instagram.com/bjptechnologies/" in data["sameAs"]
    hours = {
        d: (h["opens"], h["closes"])
        for h in data["openingHoursSpecification"]
        for d in h["dayOfWeek"]
    }
    assert hours["Monday"] == ("08:00", "18:00")
    assert hours["Saturday"] == ("08:00", "17:00")
    assert "Sunday" not in hours


@pytest.mark.django_db
def test_structured_data_not_on_every_page(client):
    html = client.get(reverse("main:about")).content.decode()
    assert "application/ld+json" not in html


@pytest.mark.django_db
def test_canonical_link_uses_main_domain(client):
    html = client.get(reverse("main:about")).content.decode()
    assert '<link rel="canonical" href="https://bjptechnologies.co.tz/about/">' in html


@pytest.mark.django_db
def test_search_console_tag_only_when_set(client):
    assert "google-site-verification" not in client.get(HOME_URL).content.decode()
    site = SiteSettings.get()
    site.google_site_verification = "abc123XYZ"
    site.save()
    html = client.get(HOME_URL).content.decode()
    assert '<meta name="google-site-verification" content="abc123XYZ">' in html


@override_settings(ALLOWED_HOSTS=["bjptechnologies.co.tz", "www.bjptechnologies.co.tz"])
def test_www_redirects_permanently_to_main_domain():
    middleware = StripWwwMiddleware(lambda request: HttpResponse("ok"))
    request = RequestFactory().get("/contact/?product=bms", HTTP_HOST="www.bjptechnologies.co.tz")
    response = middleware(request)
    assert response.status_code == 301
    assert response["Location"] == "https://bjptechnologies.co.tz/contact/?product=bms"


@override_settings(ALLOWED_HOSTS=["bjptechnologies.co.tz"])
def test_main_domain_is_served_normally():
    middleware = StripWwwMiddleware(lambda request: HttpResponse("ok"))
    request = RequestFactory().get("/", HTTP_HOST="bjptechnologies.co.tz")
    assert middleware(request).status_code == 200


def test_www_middleware_runs_first_in_production():
    from config.settings import production

    assert production.MIDDLEWARE[0] == "apps.core.middleware.StripWwwMiddleware"


@pytest.mark.django_db
def test_contact_page_hours_and_directions(client):
    html = client.get(CONTACT_URL).content.decode()
    assert "Mon – Fri &nbsp;|&nbsp; 8 AM – 6 PM" in html
    assert "Saturday &nbsp;|&nbsp; 8 AM – 5 PM" in html
    assert "Sunday &nbsp;|&nbsp; Closed" in html
    assert 'href="https://www.google.com/maps?cid=17710749172499910700"' in html
    assert "Get directions" in html


@pytest.mark.django_db
def test_footer_has_instagram_and_clean_svg_logos(client):
    html = client.get(HOME_URL).content.decode()
    assert 'href="https://www.instagram.com/bjptechnologies/"' in html
    assert "images/logo/bjp-logo-horizontal-light.svg" in html
    assert "images/logo/bjp-logo-horizontal-dark.svg" in html
    assert "bjp-logo-horizontal-light.png" not in html


@pytest.mark.django_db
def test_about_counter_no_longer_advertises_security_audits(client):
    html = client.get(reverse("main:about")).content.decode()
    assert "Systems Delivered" in html
    assert "Security Audits" not in html
