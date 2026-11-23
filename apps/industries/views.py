from django.views.generic import DetailView, ListView

from .models import Industry


class IndustriesListView(ListView):
    model = Industry
    template_name = "industries/list.html"
    context_object_name = "industries"
    queryset = Industry.objects.filter(is_active=True).order_by("order")


class IndustryDetailView(DetailView):
    model = Industry
    template_name = "industries/detail.html"
    context_object_name = "industry"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Industry.objects.filter(is_active=True).select_related("featured_product")
