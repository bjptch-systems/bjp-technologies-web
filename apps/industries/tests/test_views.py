import pytest
from django.urls import reverse

from apps.industries.models import Industry


@pytest.fixture
def industry(db):
    return Industry.objects.create(
        name="Healthcare Providers",
        slug="healthcare-providers",
        tagline="IT solutions for healthcare organisations",
        description="We help hospitals and clinics embrace digital health.",
        services_offered="Patient management\nTeleconsultation\nData security",
        is_active=True,
        order=1,
    )


@pytest.fixture
def inactive_industry(db):
    return Industry.objects.create(
        name="Hidden Industry",
        slug="hidden-industry",
        is_active=False,
    )


@pytest.mark.django_db
class TestIndustriesListView:
    def test_list_returns_200(self, client, industry):
        response = client.get(reverse("industries:list"))
        assert response.status_code == 200

    def test_list_uses_correct_template(self, client, industry):
        response = client.get(reverse("industries:list"))
        assert "industries/list.html" in [t.name for t in response.templates]

    def test_list_shows_active_industries(self, client, industry):
        response = client.get(reverse("industries:list"))
        assert industry in response.context["industries"]

    def test_list_excludes_inactive_industries(self, client, industry, inactive_industry):
        response = client.get(reverse("industries:list"))
        assert inactive_industry not in response.context["industries"]


@pytest.mark.django_db
class TestIndustryDetailView:
    def test_detail_returns_200(self, client, industry):
        response = client.get(reverse("industries:detail", kwargs={"slug": industry.slug}))
        assert response.status_code == 200

    def test_detail_uses_correct_template(self, client, industry):
        response = client.get(reverse("industries:detail", kwargs={"slug": industry.slug}))
        assert "industries/detail.html" in [t.name for t in response.templates]

    def test_detail_context_has_industry(self, client, industry):
        response = client.get(reverse("industries:detail", kwargs={"slug": industry.slug}))
        assert response.context["industry"] == industry

    def test_detail_invalid_slug_returns_404(self, client):
        response = client.get(reverse("industries:detail", kwargs={"slug": "does-not-exist"}))
        assert response.status_code == 404

    def test_inactive_industry_detail_returns_404(self, client, inactive_industry):
        response = client.get(reverse("industries:detail", kwargs={"slug": inactive_industry.slug}))
        assert response.status_code == 404

    def test_detail_shows_industry_image(self, client, industry):
        industry.image = "bjp-healthcare.webp"
        industry.save()
        response = client.get(reverse("industries:detail", kwargs={"slug": industry.slug}))
        assert "images/industry/bjp-healthcare.webp" in response.content.decode()

    def test_detail_falls_back_when_image_blank(self, client, industry):
        response = client.get(reverse("industries:detail", kwargs={"slug": industry.slug}))
        content = response.content.decode()
        assert "images/industry/bjp-industry-detail.webp" in content
        assert "images/industry/02.webp" not in content
