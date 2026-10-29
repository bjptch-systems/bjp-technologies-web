from django import forms

from apps.services.models import Service

from .models import ContactEnquiry


class ContactForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True).order_by("order", "name"),
        required=False,
        empty_label="Select a service (optional)",
    )
    consent = forms.BooleanField(
        required=True,
        error_messages={
            "required": "Please tick this box so we can respond to your enquiry.",
        },
    )

    class Meta:
        model = ContactEnquiry
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "service",
            "message",
        ]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_message(self) -> str:
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < 10:
            raise forms.ValidationError(
                "Please provide a more detailed message (at least 10 characters)."
            )
        return message

    def clean_first_name(self) -> str:
        return self.cleaned_data.get("first_name", "").strip()

    def clean_last_name(self) -> str:
        return self.cleaned_data.get("last_name", "").strip()
