import pytest
from django.urls import reverse

from apps.products.models import Product


@pytest.fixture
def live_product(db):
    return Product.objects.create(
        name="Live Product",
        slug="live-product",
        tagline="A live tagline.",
        short_description="A short description.",
        long_description="Long description paragraph.",
        status=Product.STATUS_LIVE,
        order=1,
    )


@pytest.fixture
def coming_soon_product(db):
    return Product.objects.create(
        name="Coming Soon",
        slug="coming-soon",
        status=Product.STATUS_COMING_SOON,
    )


@pytest.mark.django_db
class TestProductsListView:
    def test_list_returns_200(self, client, live_product):
        response = client.get(reverse("products:list"))
        assert response.status_code == 200

    def test_list_uses_correct_template(self, client, live_product):
        response = client.get(reverse("products:list"))
        assert "products/list.html" in [t.name for t in response.templates]

    def test_list_shows_live_products(self, client, live_product):
        response = client.get(reverse("products:list"))
        assert live_product in response.context["products"]

    def test_list_excludes_coming_soon_products(self, client, live_product, coming_soon_product):
        response = client.get(reverse("products:list"))
        assert coming_soon_product not in response.context["products"]


@pytest.mark.django_db
class TestProductDetailView:
    def test_detail_returns_200(self, client, live_product):
        response = client.get(reverse("products:detail", kwargs={"slug": live_product.slug}))
        assert response.status_code == 200

    def test_detail_uses_correct_template(self, client, live_product):
        response = client.get(reverse("products:detail", kwargs={"slug": live_product.slug}))
        assert "products/detail.html" in [t.name for t in response.templates]

    def test_detail_context_has_product(self, client, live_product):
        response = client.get(reverse("products:detail", kwargs={"slug": live_product.slug}))
        assert response.context["product"] == live_product

    def test_detail_context_has_other_products(self, client, live_product):
        other = Product.objects.create(name="Other", slug="other", status=Product.STATUS_LIVE)
        response = client.get(reverse("products:detail", kwargs={"slug": live_product.slug}))
        other_products = list(response.context["other_products"])
        assert other in other_products
        assert live_product not in other_products

    def test_detail_invalid_slug_returns_404(self, client):
        response = client.get(reverse("products:detail", kwargs={"slug": "does-not-exist"}))
        assert response.status_code == 404

    def test_coming_soon_detail_returns_404(self, client, coming_soon_product):
        response = client.get(reverse("products:detail", kwargs={"slug": coming_soon_product.slug}))
        assert response.status_code == 404

    def test_contact_block_hidden_when_empty(self, client, live_product):
        response = client.get(reverse("products:detail", kwargs={"slug": live_product.slug}))
        assert b"Talk to the" not in response.content

    def test_contact_block_visible_when_email_set(self, client, live_product):
        live_product.contact_email = "support@example.com"
        live_product.save()
        response = client.get(reverse("products:detail", kwargs={"slug": live_product.slug}))
        assert b"support@example.com" in response.content


@pytest.mark.django_db
class TestNavbarIntegration:
    def test_navbar_contains_products_link_on_home(self, client, live_product):
        response = client.get(reverse("main:home"))
        assert response.status_code == 200
        assert reverse("products:list").encode() in response.content
        assert b">Products<" in response.content

    def test_home_page_shows_live_products_strip(self, client, live_product):
        response = client.get(reverse("main:home"))
        assert live_product in response.context["products"]

    def test_home_page_excludes_coming_soon_from_strip(
        self, client, live_product, coming_soon_product
    ):
        response = client.get(reverse("main:home"))
        assert coming_soon_product not in response.context["products"]


@pytest.mark.django_db
class TestPMSDetailPage:
    """The PMS record from migration 0002 must render its detail page end-to-end."""

    def test_pms_detail_renders(self, client):
        response = client.get(reverse("products:detail", kwargs={"slug": "pms"}))
        assert response.status_code == 200

    def test_pms_detail_shows_tagline(self, client):
        response = client.get(reverse("products:detail", kwargs={"slug": "pms"}))
        assert b"Property management, finally simple." in response.content

    def test_pms_detail_shows_features(self, client):
        response = client.get(reverse("products:detail", kwargs={"slug": "pms"}))
        assert b"Property &amp; unit inventory" in response.content
        assert b"Invoicing &amp; receipts" in response.content

    def test_pms_detail_cta_opens_in_new_tab(self, client):
        response = client.get(reverse("products:detail", kwargs={"slug": "pms"}))
        assert b'target="_blank"' in response.content
        assert b"https://pms.bjptechnologies.co.tz" in response.content
