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
