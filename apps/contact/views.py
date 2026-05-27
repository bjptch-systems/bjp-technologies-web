from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models import ContactEnquiry


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact:success")

    def _get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return self.request.META.get("REMOTE_ADDR", "")

    def _is_rate_limited(self, ip: str) -> bool:
        cutoff = timezone.now() - timedelta(minutes=30)
        return (
            ContactEnquiry.objects.filter(
                ip_address=ip,
                created_at__gte=cutoff,
            ).count()
            >= 5
        )

    def form_valid(self, form):
        ip = self._get_client_ip()
        if self._is_rate_limited(ip):
            form.add_error(
                None,
                "Too many submissions from your network. Please try again in 30 minutes.",
            )
            return self.form_invalid(form)

        enquiry = form.save(commit=False)
        enquiry.ip_address = ip
        enquiry.save()

        self._send_notification(enquiry)
        self._send_confirmation(enquiry)

        return super().form_valid(form)

    def _send_notification(self, enquiry: ContactEnquiry) -> None:
        service_name = enquiry.service.name if enquiry.service else "Not specified"
        subject = f"New Enquiry from {enquiry.full_name} — BJP Technologies"
        body = (
            f"New contact enquiry received.\n\n"
            f"Name:    {enquiry.full_name}\n"
            f"Email:   {enquiry.email}\n"
            f"Phone:   {enquiry.phone or 'Not provided'}\n"
            f"Company: {enquiry.company or 'Not provided'}\n"
            f"Service: {service_name}\n\n"
            f"Message:\n{enquiry.message}\n\n"
            f"---\n"
            f"IP Address: {enquiry.ip_address}\n"
            f"Submitted:  {enquiry.created_at.strftime('%Y-%m-%d %H:%M')} EAT\n\n"
            f"Reply directly to this email to respond to the enquirer."
        )
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[enquiry.email],
        )
        email.send(fail_silently=True)

    def _send_confirmation(self, enquiry: ContactEnquiry) -> None:
        preview = enquiry.message[:200] + ("..." if len(enquiry.message) > 200 else "")
        subject = "We received your message — BJP Technologies"
        body = (
            f"Dear {enquiry.first_name},\n\n"
            f"Thank you for contacting BJP Technologies. We have received your enquiry "
            f"and will respond within 1–2 business days.\n\n"
            f'Your message:\n"{preview}"\n\n'
            f"For urgent matters, please call us directly at +255 678 290 994.\n\n"
            f"Best regards,\n"
            f"BJP Technologies (T) Limited\n"
            f"info@bjptechnologies.co.tz | +255 678 290 994\n"
            f"Ubungo, Dar es Salaam, Tanzania"
        )
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[enquiry.email],
        )
        email.send(fail_silently=True)


class ContactSuccessView(TemplateView):
    template_name = "contact/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fire the GA4 conversion event on the success page. The base template
        # only emits the gtag('event', ...) call when analytics_enabled is true.
        context["ga_event"] = "contact_submit"
        return context
