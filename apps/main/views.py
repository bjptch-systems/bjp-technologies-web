from django.views.generic import TemplateView

from apps.industries.models import Industry
from apps.products.models import Product
from apps.services.models import Service


class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["industries"] = Industry.objects.filter(is_active=True).order_by("order")
        context["featured_services"] = Service.objects.filter(is_active=True).order_by("order")
        context["products"] = Product.objects.filter(status=Product.STATUS_LIVE).order_by("order")
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(is_active=True).order_by("order")
        return context
