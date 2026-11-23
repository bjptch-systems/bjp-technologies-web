import pytest


@pytest.mark.django_db
def test_home_page_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_about_page_returns_200(client):
    response = client.get("/about/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_product_showcase_lists_every_live_product(client):
    from apps.products.models import Product

    html = client.get("/").content.decode()
    live = Product.objects.filter(status=Product.STATUS_LIVE)
    assert html.count('role="tab"') == live.count()
    assert html.count('role="tabpanel"') == live.count()
    for product in live:
        assert f'id="ps-panel-{product.slug}"' in html
        assert f"Explore {product.short_name}" in html
    assert "js/products-showcase.js" in html


@pytest.mark.django_db
def test_product_short_names():
    from apps.products.models import Product

    names = dict(Product.objects.values_list("slug", "name"))
    shorts = {p.slug: p.short_name for p in Product.objects.all()}
    assert shorts["pms"] == "PMS"
    assert shorts["vikundi"] == "Vikundi"
    assert shorts["smart-pos"] == "Smart POS" == names["smart-pos"]
