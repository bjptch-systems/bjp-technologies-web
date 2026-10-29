import pytest

from apps.contact.forms import ContactForm
from apps.services.models import Service


@pytest.fixture
def service(db):
    return Service.objects.create(name="Software Development", order=1)


def valid_data(service=None):
    return {
        "first_name": "Fatuma",
        "last_name": "Ally",
        "email": "fatuma@example.com",
        "phone": "+255711000001",
        "company": "MyBiz Ltd",
        "service": service.pk if service else "",
        "message": "I need help with our payroll system.",
        "consent": "on",
    }


@pytest.mark.django_db
def test_valid_form(service):
    form = ContactForm(data=valid_data(service))
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_valid_without_optional_fields(db):
    data = {
        "first_name": "Omar",
        "last_name": "Bakari",
        "email": "omar@example.com",
        "phone": "",
        "company": "",
        "service": "",
        "message": "A simple enquiry about services.",
        "consent": "on",
    }
    form = ContactForm(data=data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_first_name_required(db):
    data = valid_data()
    data["first_name"] = ""
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "first_name" in form.errors


@pytest.mark.django_db
def test_last_name_required(db):
    data = valid_data()
    data["last_name"] = ""
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "last_name" in form.errors


@pytest.mark.django_db
def test_email_required(db):
    data = valid_data()
    data["email"] = ""
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_invalid_email(db):
    data = valid_data()
    data["email"] = "not-an-email"
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_message_required(db):
    data = valid_data()
    data["message"] = ""
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "message" in form.errors


@pytest.mark.django_db
def test_message_too_short(db):
    data = valid_data()
    data["message"] = "short"
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "message" in form.errors


@pytest.mark.django_db
def test_message_minimum_length(db):
    data = valid_data()
    data["message"] = "1234567890"
    form = ContactForm(data=data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_service_optional(db):
    data = valid_data()
    data["service"] = ""
    form = ContactForm(data=data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["service"] is None


@pytest.mark.django_db
def test_consent_required(service):
    data = valid_data(service)
    del data["consent"]
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert form.errors["consent"] == ["Please tick this box so we can respond to your enquiry."]
