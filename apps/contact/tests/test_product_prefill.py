"""Tests for /contact/?product=… prefill behaviour.

Product detail pages route their "Request a demo" CTA to the BJP contact
form, not to the external product domain (per user direction). The
contact view reads ?product= and prefills the message and shows a
small banner so the visitor knows the form remembers which product
they came from.
"""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_bms_hint_prefills_message_and_renders_banner(client):
    resp = client.get(reverse("contact:contact") + "?product=bms")
    assert resp.status_code == 200
    assert resp.context["product_hint"] is not None
    assert resp.context["product_hint"].slug == "bms"
    # Initial value of the message field carries the demo-request line
    assert b"BMS (Business Management System)" in resp.content
    # Banner is rendered
    assert b"Requesting a demo of" in resp.content


@pytest.mark.django_db
def test_vikundi_hint_prefills_message_and_renders_banner(client):
    resp = client.get(reverse("contact:contact") + "?product=vikundi")
    assert resp.status_code == 200
    assert resp.context["product_hint"] is not None
    assert resp.context["product_hint"].slug == "vikundi"
    assert b"Vikundi" in resp.content


@pytest.mark.django_db
def test_unknown_product_param_is_ignored(client):
    resp = client.get(reverse("contact:contact") + "?product=not-a-product")
    assert resp.status_code == 200
    assert resp.context.get("product_hint") is None
    assert b"Requesting a demo of" not in resp.content


@pytest.mark.django_db
def test_no_product_param_renders_clean_form(client):
    resp = client.get(reverse("contact:contact"))
    assert resp.status_code == 200
    assert resp.context.get("product_hint") is None
    assert b"Requesting a demo of" not in resp.content
