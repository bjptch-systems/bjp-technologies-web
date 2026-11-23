"""Release 2 (Nov 2026) fixes: page caching, uploaded logo colours, contact dropdown,
static files storage, and the Retail industry → Smart POS link."""

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.core.models import SiteSettings


@pytest.mark.django_db
@pytest.mark.parametrize("url_name", ["main:home", "products:list", "contact:contact"])
def test_html_pages_are_not_kept_by_shared_caches(client, url_name):
    response = client.get(reverse(url_name))
    cache_control = response["Cache-Control"]
    assert "private" in cache_control
    assert "no-cache" in cache_control


def test_no_cache_middleware_is_active_in_production_too(monkeypatch):
    import importlib

    monkeypatch.setenv("ALLOWED_HOSTS", "bjptechnologies.co.tz")
    production = importlib.import_module("config.settings.production")
    assert "apps.core.middleware.NoCacheHTMLMiddleware" in production.MIDDLEWARE


@pytest.mark.django_db
def test_uploaded_logo_keeps_its_own_colours(client, tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    site = SiteSettings.get()
    site.logo = SimpleUploadedFile("logo.svg", b"<svg xmlns='http://www.w3.org/2000/svg'/>")
    site.save()
    html = client.get(reverse("main:home")).content.decode()
    assert site.logo.url in html
    assert "brightness(0) invert(1)" not in html


@pytest.mark.django_db
def test_contact_service_dropdown_has_no_broken_inline_style(client):
    html = client.get(reverse("contact:contact")).content.decode()
    assert 'class="contact-service-select"' in html
    assert 'url(\\"' not in html


def test_static_storage_uses_the_setting_django_reads():
    assert (
        settings.STORAGES["staticfiles"]["BACKEND"]
        == "whitenoise.storage.CompressedStaticFilesStorage"
    )


@pytest.fixture
def retail(db):
    from apps.industries.models import Industry
    from apps.products.models import Product

    return Industry.objects.create(
        name="Retail & Wholesale Businesses",
        slug="retail-wholesale",
        featured_product=Product.objects.get(slug="smart-pos"),
    )


@pytest.mark.django_db
def test_retail_industry_recommends_smart_pos(client, retail):
    html = client.get(reverse("industries:detail", kwargs={"slug": retail.slug})).content.decode()
    assert "Recommended for" in html
    assert reverse("products:detail", kwargs={"slug": "smart-pos"}) in html
    assert "https://bms.bjptechnologies.co.tz/register?product=bms_shop" in html


@pytest.mark.django_db
def test_other_industries_show_no_product_callout(client):
    from apps.industries.models import Industry

    Industry.objects.create(name="Healthcare Providers", slug="healthcare")
    html = client.get(reverse("industries:detail", kwargs={"slug": "healthcare"})).content.decode()
    assert "Recommended for" not in html
