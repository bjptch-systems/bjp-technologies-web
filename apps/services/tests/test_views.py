import pytest
from django.urls import reverse

from apps.services.models import Service


@pytest.fixture
def service(db):
    return Service.objects.create(
        name="Software Development",
        slug="software-development",
        tagline="Custom software for your business",
        description="We build custom web applications.",
        bullet_points="Custom web apps\nERP systems\nAPI integrations",
        is_active=True,
        order=1,
    )


@pytest.fixture
def inactive_service(db):
    return Service.objects.create(
        name="Hidden Service",
        slug="hidden-service",
        is_active=False,
    )


@pytest.mark.django_db
class TestServicesListView:
    def test_list_returns_200(self, client, service):
        response = client.get(reverse("services:list"))
        assert response.status_code == 200

    def test_list_uses_correct_template(self, client, service):
        response = client.get(reverse("services:list"))
        assert "services/list.html" in [t.name for t in response.templates]

    def test_list_shows_active_services(self, client, service):
        response = client.get(reverse("services:list"))
        assert service in response.context["services"]

    def test_list_excludes_inactive_services(self, client, service, inactive_service):
        response = client.get(reverse("services:list"))
        assert inactive_service not in response.context["services"]


@pytest.mark.django_db
class TestServiceDetailView:
    def test_detail_returns_200(self, client, service):
        response = client.get(reverse("services:detail", kwargs={"slug": service.slug}))
        assert response.status_code == 200

    def test_detail_uses_correct_template(self, client, service):
        response = client.get(reverse("services:detail", kwargs={"slug": service.slug}))
        assert "services/detail.html" in [t.name for t in response.templates]

    def test_detail_context_has_service(self, client, service):
        response = client.get(reverse("services:detail", kwargs={"slug": service.slug}))
        assert response.context["service"] == service

    def test_detail_context_has_other_services(self, client, service):
        other = Service.objects.create(name="Other", slug="other", is_active=True, order=2)
        response = client.get(reverse("services:detail", kwargs={"slug": service.slug}))
        other_services = list(response.context["other_services"])
        assert other in other_services
        assert service not in other_services

    def test_detail_invalid_slug_returns_404(self, client):
        response = client.get(reverse("services:detail", kwargs={"slug": "does-not-exist"}))
        assert response.status_code == 404

    def test_inactive_service_redirects_to_services_list(self, client, inactive_service):
        """Paused services keep old links working by sending them to the list (302,
        temporary, so the page can return if the service is switched back on)."""
        response = client.get(reverse("services:detail", kwargs={"slug": inactive_service.slug}))
        assert response.status_code == 302
        assert response["Location"] == reverse("services:list")

    def test_detail_shows_service_image(self, client, service):
        service.image = "bjp-software-development.webp"
        service.save()
        response = client.get(reverse("services:detail", kwargs={"slug": service.slug}))
        assert "images/service/bjp-software-development.webp" in response.content.decode()

    def test_detail_falls_back_when_image_blank(self, client, service):
        response = client.get(reverse("services:detail", kwargs={"slug": service.slug}))
        assert "images/service/bjp-services.webp" in response.content.decode()


@pytest.mark.django_db
class TestServiceLineup:
    """Nov 2026: Cloud & Infrastructure and Cybersecurity paused, Bulk SMS added."""

    def test_bulk_sms_page_is_live(self, client):
        response = client.get(reverse("services:detail", kwargs={"slug": "bulk-sms"}))
        assert response.status_code == 200
        html = response.content.decode()
        assert "Custom Sender ID" in html
        assert "SMS API" in html
        assert "images/service/bjp-bulk-sms.webp" in html

    def test_navbar_lists_active_services_only(self, client, service, inactive_service):
        html = client.get(reverse("main:home")).content.decode()
        assert reverse("services:detail", kwargs={"slug": "bulk-sms"}) in html
        assert reverse("services:detail", kwargs={"slug": service.slug}) in html
        assert reverse("services:detail", kwargs={"slug": inactive_service.slug}) not in html

    @pytest.mark.parametrize(
        "url_name", ["main:home", "main:about", "services:list", "contact:contact"]
    )
    def test_public_pages_no_longer_advertise_paused_services(self, client, url_name):
        html = client.get(reverse(url_name)).content.decode().lower()
        assert "cybersecurity" not in html
        assert "cloud infrastructure" not in html
        assert "vapt" not in html

    def test_services_list_icons_are_icon_classes_not_filenames(self, client):
        html = client.get(reverse("services:list")).content.decode()
        assert 'class="fa-regular fa-comment-sms"' in html
        assert 'class="22.svg"' not in html
