"""Regression tests for the Product admin.

The headline test is `test_changelist_renders` — Django 6 hardened
`format_html`, so calling it with zero args raises TypeError. The
`show_contact_state` method used to do exactly that and 500'd the
changelist on production. This test catches a regression by actually
rendering the changelist.
"""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_changelist_renders(admin_client):
    """The Product admin changelist must render with the seeded PMS row.

    Catches the regression where show_contact_state used `format_html(...)`
    with no args — Django 6 raises `TypeError: args or kwargs must be
    provided.` on that pattern.
    """
    url = reverse("admin:products_product_changelist")
    resp = admin_client.get(url)
    assert resp.status_code == 200
    assert b"PMS by BJP Technologies" in resp.content
    # show_contact_state output is rendered for each row
    assert b"empty" in resp.content or b"filled" in resp.content


@pytest.mark.django_db
def test_change_form_renders(admin_client):
    """The Product change form must render for the seeded PMS row."""
    from apps.products.models import Product

    pms = Product.objects.get(slug="pms")
    url = reverse("admin:products_product_change", args=[pms.pk])
    resp = admin_client.get(url)
    assert resp.status_code == 200
    assert b"PMS by BJP Technologies" in resp.content
