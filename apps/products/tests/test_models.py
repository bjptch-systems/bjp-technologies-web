import re

import pytest

from apps.products.models import Product


@pytest.mark.django_db
class TestProductModel:
    def test_str(self):
        p = Product.objects.create(name="My Test Product")
        assert str(p) == "My Test Product"

    def test_slug_auto_generated(self):
        p = Product.objects.create(name="Property Management System")
        assert p.slug == "property-management-system"

    def test_slug_not_overwritten_on_save(self):
        p = Product.objects.create(name="Test", slug="custom-slug")
        p.save()
        assert p.slug == "custom-slug"

    def test_is_live_default(self):
        p = Product.objects.create(name="Live by default")
        assert p.is_live is True
        assert p.status == Product.STATUS_LIVE

    def test_is_live_false_when_coming_soon(self):
        p = Product.objects.create(name="Future", status=Product.STATUS_COMING_SOON)
        assert p.is_live is False

    def test_has_contact_block_false_when_empty(self):
        p = Product.objects.create(name="Empty contacts")
        assert p.has_contact_block is False

    def test_has_contact_block_true_when_email_set(self):
        p = Product.objects.create(name="With email", contact_email="support@example.com")
        assert p.has_contact_block is True

    def test_has_contact_block_true_when_only_phone_set(self):
        p = Product.objects.create(name="With phone", contact_phone="+255700000000")
        assert p.has_contact_block is True

    def test_has_contact_block_true_when_only_hours_set(self):
        p = Product.objects.create(name="With hours", contact_hours="Mon-Fri 9-5")
        assert p.has_contact_block is True

    def test_has_contact_block_true_when_only_whatsapp_set(self):
        p = Product.objects.create(name="With wa", contact_whatsapp="+255700000000")
        assert p.has_contact_block is True

    def test_get_problem_list_parses_lines(self):
        p = Product.objects.create(name="P", problem_statements="A\nB\nC")
        assert p.get_problem_list() == ["A", "B", "C"]

    def test_get_problem_list_strips_blanks(self):
        p = Product.objects.create(name="P", problem_statements="A\n\nB\n")
        assert p.get_problem_list() == ["A", "B"]

    def test_get_target_users_list(self):
        p = Product.objects.create(name="P", target_users="Landlord — track rent\nAgent — manage")
        assert p.get_target_users_list() == [
            "Landlord — track rent",
            "Agent — manage",
        ]

    def test_get_differentiators_list(self):
        p = Product.objects.create(name="P", differentiators="One\nTwo")
        assert p.get_differentiators_list() == ["One", "Two"]

    def test_get_how_it_works_list(self):
        p = Product.objects.create(name="P", how_it_works_steps="Step one\nStep two")
        assert p.get_how_it_works_list() == ["Step one", "Step two"]

    def test_features_defaults_to_empty_list(self):
        p = Product.objects.create(name="P")
        assert p.features == []

    def test_features_stored_as_json(self):
        feats = [{"name": "X", "description": "y", "icon": "bi-x"}]
        p = Product.objects.create(name="P", features=feats)
        p.refresh_from_db()
        assert p.features == feats

    def test_has_created_at_and_updated_at(self):
        p = Product.objects.create(name="Timestamped")
        assert p.created_at is not None
        assert p.updated_at is not None


@pytest.mark.django_db
class TestPMSSeed:
    """The PMS record is seeded by migration 0002_seed_pms. These assert the seed exists
    and carries the brief's content — so a future seed regression is caught."""

    def test_pms_record_exists(self):
        assert Product.objects.filter(slug="pms").exists()

    def test_pms_is_live(self):
        pms = Product.objects.get(slug="pms")
        assert pms.is_live

    def test_pms_has_expected_feature_count(self):
        pms = Product.objects.get(slug="pms")
        assert len(pms.features) == 8

    def test_pms_has_contact_block_empty_until_admin_fills_it(self):
        """Brief Section 12 lists contact details as TODO — they intentionally start empty."""
        pms = Product.objects.get(slug="pms")
        assert pms.has_contact_block is False

    def test_pms_cta_urls_point_to_live_site(self):
        pms = Product.objects.get(slug="pms")
        assert pms.cta_primary_url == "https://pms.bjptechnologies.co.tz"
        assert pms.cta_secondary_url == "https://pms.bjptechnologies.co.tz"

    def test_pms_icons_use_font_awesome_not_bootstrap_icons(self):
        """After migration 0003, every PMS feature icon must use Font Awesome.

        Bootstrap Icons (`bi-*`) were loaded from a CDN that's blocked by the
        site CSP, so glyphs never rendered. Font Awesome Pro is already loaded
        site-wide via static/css/plugins/fontawesome.css.
        """
        pms = Product.objects.get(slug="pms")
        for feat in pms.features:
            icon = feat.get("icon", "")
            assert icon.startswith("fa-"), f"Expected fa-* icon, got: {icon!r}"
            assert "bi-" not in icon, f"Leftover Bootstrap Icons class: {icon!r}"


@pytest.mark.django_db
class TestBMSSeed:
    def test_bms_record_exists(self):
        assert Product.objects.filter(slug="bms").exists()

    def test_bms_is_live(self):
        bms = Product.objects.get(slug="bms")
        assert bms.is_live

    def test_bms_is_now_smart_bms(self):
        """Release 2 (Nov 2026): renamed and rewritten from bms.bjptechnologies.co.tz."""
        bms = Product.objects.get(slug="bms")
        assert bms.name == "Smart BMS"
        assert len(bms.features) == 8
        assert bms.screenshots == []  # no mock-ups shown as the real product

    def test_bms_drops_claims_the_product_site_does_not_make(self):
        bms = Product.objects.get(slug="bms")
        text = " ".join(
            [bms.short_description, bms.long_description, bms.differentiators, str(bms.features)]
        ).lower()
        for claim in ("mobile money", "mobile-money", "vat", "tin", "low-stock", "reorder"):
            assert not re.search(rf"\b{claim}\b", text), claim

    def test_bms_does_not_advertise_loans_feature(self):
        bms = Product.objects.get(slug="bms")
        names = [f.get("name", "") for f in bms.features]
        assert "Loans / Microfinance" not in names

    def test_bms_icons_use_font_awesome_not_bootstrap_icons(self):
        bms = Product.objects.get(slug="bms")
        for feat in bms.features:
            icon = feat.get("icon", "")
            assert icon.startswith("fa-"), f"Expected fa-* icon, got: {icon!r}"
            assert "bi-" not in icon, f"Leftover bi-* class: {icon!r}"

    def test_bms_ctas_go_to_the_product_site(self):
        """Nov 2026 decision (replaces the earlier 'hide the live URL' rule): the
        product site is public, so the buttons start a trial and show prices there."""
        bms = Product.objects.get(slug="bms")
        assert bms.cta_primary_label == "Start free trial"
        assert bms.cta_primary_url == "https://bms.bjptechnologies.co.tz/register?product=bms_full"
        assert bms.cta_secondary_url == "https://bms.bjptechnologies.co.tz/pricing"

    def test_bms_uses_company_support_email(self):
        bms = Product.objects.get(slug="bms")
        assert bms.contact_email == "info@bjptechnologies.co.tz"

    def test_bms_has_no_disclosures(self):
        bms = Product.objects.get(slug="bms")
        assert bms.get_disclosures_list() == []


@pytest.mark.django_db
class TestVikundiSeed:
    def test_vikundi_record_exists(self):
        assert Product.objects.filter(slug="vikundi").exists()

    def test_vikundi_is_live(self):
        v = Product.objects.get(slug="vikundi")
        assert v.is_live

    def test_vikundi_has_12_features(self):
        v = Product.objects.get(slug="vikundi")
        assert len(v.features) == 12

    def test_vikundi_keeps_honest_tone_disclosures(self):
        """Vikundi brief explicitly flags two limitations — they must be
        carried into the public page so we don't oversell."""
        v = Product.objects.get(slug="vikundi")
        notes = v.get_disclosures_list()
        assert len(notes) == 2
        all_text = " ".join(notes).lower()
        assert "single group" in all_text
        assert "share-out" in all_text or "automated" in all_text

    def test_vikundi_cta_routes_to_internal_contact_form(self):
        v = Product.objects.get(slug="vikundi")
        assert v.cta_primary_url == "/contact/?product=vikundi"
        assert "bjptechnologies.co.tz" not in v.cta_primary_url
        assert v.cta_secondary_url == ""

    def test_vikundi_uses_company_support_email(self):
        v = Product.objects.get(slug="vikundi")
        assert v.contact_email == "info@bjptechnologies.co.tz"


@pytest.mark.django_db
class TestProductsOrdering:
    """The home-page strip and list page order products by `order`. Confirm
    PMS=1, BMS=2, Vikundi=3 to lock the intended layout."""

    def test_live_products_are_ordered(self):
        slugs = list(
            Product.objects.filter(status=Product.STATUS_LIVE)
            .order_by("order")
            .values_list("slug", flat=True)
        )
        assert slugs == ["pms", "smart-pos", "smart-restaurant", "bms", "vikundi", "lms"]


@pytest.mark.django_db
class TestSmartPOSSeed:
    def test_smart_pos_is_live_and_shops_only(self):
        pos = Product.objects.get(slug="smart-pos")
        assert pos.is_live
        names = [f["name"] for f in pos.features]
        assert "Sell by weight or volume" in names
        assert "Kitchen screen" not in names
        text = " ".join(
            [pos.tagline, pos.short_description, pos.long_description, pos.target_users]
        ).lower()
        assert "restaurant" not in text
        assert pos.screenshots == []

    def test_smart_pos_ctas_go_to_the_product_site(self):
        pos = Product.objects.get(slug="smart-pos")
        assert pos.cta_primary_url == "https://bms.bjptechnologies.co.tz/register?product=bms_shop"
        assert pos.cta_secondary_url == "https://bms.bjptechnologies.co.tz/pricing"

    def test_smart_pos_assets_exist(self):
        from pathlib import Path

        from django.conf import settings

        pos = Product.objects.get(slug="smart-pos")
        rest = Product.objects.get(slug="smart-restaurant")
        bms = Product.objects.get(slug="bms")
        for rel in (
            pos.hero_image,
            pos.logo_image,
            rest.hero_image,
            rest.logo_image,
            bms.hero_image,
            bms.logo_image,
        ):
            assert (Path(settings.BASE_DIR) / "static" / "images" / rel).exists(), rel


@pytest.mark.django_db
class TestSmartRestaurantSeed:
    def test_smart_restaurant_is_live_with_kitchen_features(self):
        rest = Product.objects.get(slug="smart-restaurant")
        assert rest.is_live
        assert rest.short_name == "Smart Restaurant"
        names = [f["name"] for f in rest.features]
        for feature in ("Tables and orders", "Kitchen screen", "QR menu at the table"):
            assert feature in names
        assert rest.screenshots == []
        assert rest.icon == "fa-regular fa-utensils"

    def test_smart_restaurant_trial_opens_restaurant_sign_up(self):
        rest = Product.objects.get(slug="smart-restaurant")
        assert rest.cta_primary_url == (
            "https://bms.bjptechnologies.co.tz/register?product=bms_shop&business=restaurant"
        )
        assert rest.cta_secondary_url == "https://bms.bjptechnologies.co.tz/pricing"


@pytest.mark.django_db
class TestLmsSeed:
    def test_lms_is_live_and_books_a_demo(self):
        lms = Product.objects.get(slug="lms")
        assert lms.is_live
        assert lms.short_name == "LMS"
        assert lms.cta_primary_label == "Book a demo"
        assert lms.cta_primary_url == "/contact/?product=lms"
        assert lms.cta_secondary_url == ""
        assert lms.pricing_summary.startswith("Price on request")

    def test_lms_has_no_live_screenshots_or_unconfirmed_integrations(self):
        """Screenshots of the live system would show a client's customers, and the
        bureau, banking and gateway links are not confirmed connected."""
        lms = Product.objects.get(slug="lms")
        assert lms.screenshots == []
        text = " ".join(
            [lms.long_description, lms.differentiators]
            + [f["name"] + " " + f["description"] for f in lms.features]
        ).lower()
        for claim in ("credit bureau", "payment gateway", "open banking"):
            assert claim not in text


@pytest.mark.django_db
def test_no_product_uses_icons_missing_from_the_font():
    """fa-display and fa-people-group exist in the CSS but have no glyph in the
    site's Font Awesome build, so they render blank."""
    blank = {"fa-regular fa-display", "fa-regular fa-people-group"}
    for product in Product.objects.all():
        assert product.icon not in blank, product.slug
        for feature in product.features:
            assert feature.get("icon") not in blank, (product.slug, feature["name"])
