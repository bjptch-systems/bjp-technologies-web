from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from .models import Service


class ServicesListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    queryset = Service.objects.filter(is_active=True).order_by("order")


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        # A paused (inactive) service sends old links and bookmarks to the services list
        # instead of a 404. Temporary (302) so the page can come back if re-enabled.
        slug = kwargs.get(self.slug_url_kwarg)
        if Service.objects.filter(slug=slug, is_active=False).exists():
            return redirect("services:list")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["other_services"] = (
            Service.objects.filter(is_active=True).exclude(pk=self.object.pk).order_by("order")
        )
        return context
