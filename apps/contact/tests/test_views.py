from datetime import timedelta
from unittest.mock import patch

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.contact.models import ContactEnquiry
from apps.services.models import Service

CONTACT_URL = reverse("contact:contact")
SUCCESS_URL = reverse("contact:success")


@pytest.fixture
def service(db):
    return Service.objects.create(name="Cloud Infrastructure", order=1)


def post_data(service=None):
    return {
        "first_name": "Zawadi",
        "last_name": "Mtui",
        "email": "zawadi@example.com",
        "phone": "+255712000001",
        "company": "Acme Ltd",
        "service": service.pk if service else "",
        "message": "We are looking for a cloud partner in Tanzania.",
    }


# --- GET tests ---


@pytest.mark.django_db
def test_contact_get_200(client):
    response = client.get(CONTACT_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_uses_correct_template(client):
    response = client.get(CONTACT_URL)
    assert "contact/contact.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_success_get_200(client):
    response = client.get(SUCCESS_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_uses_correct_template(client):
    response = client.get(SUCCESS_URL)
    assert "contact/success.html" in [t.name for t in response.templates]


# --- POST valid ---


@pytest.mark.django_db
def test_valid_post_redirects_to_success(client, service):
    with patch("apps.contact.views.ContactView._send_notification"):
        with patch("apps.contact.views.ContactView._send_confirmation"):
            response = client.post(CONTACT_URL, data=post_data(service))
    assert response.status_code == 302
    assert response["Location"] == SUCCESS_URL


@pytest.mark.django_db
def test_valid_post_creates_enquiry(client, service):
    with patch("apps.contact.views.ContactView._send_notification"):
        with patch("apps.contact.views.ContactView._send_confirmation"):
            client.post(CONTACT_URL, data=post_data(service))
    assert ContactEnquiry.objects.filter(email="zawadi@example.com").exists()


@pytest.mark.django_db
def test_enquiry_captures_ip(client, service):
    with patch("apps.contact.views.ContactView._send_notification"):
        with patch("apps.contact.views.ContactView._send_confirmation"):
            client.post(
                CONTACT_URL,
                data=post_data(service),
                REMOTE_ADDR="203.0.113.10",
            )
    enquiry = ContactEnquiry.objects.get(email="zawadi@example.com")
    assert enquiry.ip_address == "203.0.113.10"


@pytest.mark.django_db
def test_enquiry_status_defaults_new(client, service):
    with patch("apps.contact.views.ContactView._send_notification"):
        with patch("apps.contact.views.ContactView._send_confirmation"):
            client.post(CONTACT_URL, data=post_data(service))
    enquiry = ContactEnquiry.objects.get(email="zawadi@example.com")
    assert enquiry.status == ContactEnquiry.STATUS_NEW


# --- POST invalid ---


@pytest.mark.django_db
def test_invalid_post_returns_200_with_errors(client):
    response = client.post(CONTACT_URL, data={"first_name": "", "email": "bad"})
    assert response.status_code == 200
    assert response.context["form"].errors


@pytest.mark.django_db
def test_short_message_fails(client):
    data = post_data()
    data["message"] = "too short"
    response = client.post(CONTACT_URL, data=data)
    assert response.status_code == 200
    assert "message" in response.context["form"].errors


# --- Rate limiting ---


@pytest.mark.django_db
def test_rate_limit_blocks_after_five_submissions(client, db):
    ip = "198.51.100.1"
    for i in range(5):
        ContactEnquiry.objects.create(
            first_name=f"Spam{i}",
            last_name="Bot",
            email=f"spam{i}@test.com",
            message="Repeated message here.",
            ip_address=ip,
        )
    data = post_data()
    response = client.post(CONTACT_URL, data=data, REMOTE_ADDR=ip)
    assert response.status_code == 200
    assert response.context["form"].non_field_errors()


@pytest.mark.django_db
def test_rate_limit_resets_after_window(client, db):
    ip = "198.51.100.2"
    old_time = timezone.now() - timedelta(minutes=35)
    for i in range(5):
        e = ContactEnquiry.objects.create(
            first_name=f"Old{i}",
            last_name="Submission",
            email=f"old{i}@test.com",
            message="Old message from outside the window.",
            ip_address=ip,
        )
        ContactEnquiry.objects.filter(pk=e.pk).update(created_at=old_time)

    with patch("apps.contact.views.ContactView._send_notification"):
        with patch("apps.contact.views.ContactView._send_confirmation"):
            response = client.post(CONTACT_URL, data=post_data(), REMOTE_ADDR=ip)
    assert response.status_code == 302


# --- Company phone ---


@pytest.mark.django_db
def test_confirmation_email_uses_company_phone(client, service, mailoutbox):
    from apps.core.models import SiteSettings

    settings_obj = SiteSettings.get()
    settings_obj.phone = "+255 764 764 011"
    settings_obj.save()
    client.post(CONTACT_URL, post_data(service))
    confirmation = next(m for m in mailoutbox if m.to == ["zawadi@example.com"])
    assert "+255 764 764 011" in confirmation.body
    assert "678 290 994" not in confirmation.body


@pytest.mark.django_db
def test_success_page_shows_company_phone(client):
    response = client.get(SUCCESS_URL)
    assert "+255 764 764 011" in response.content.decode()
    assert 'href="tel:+255764764011"' in response.content.decode()
