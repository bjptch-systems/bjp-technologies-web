from django.views.generic import DetailView, ListView

from .models import Product


class ProductsListView(ListView):
    model = Product
    template_name = "products/list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(status=Product.STATUS_LIVE).order_by("order")


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.filter(status=Product.STATUS_LIVE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["other_products"] = (
            Product.objects.filter(status=Product.STATUS_LIVE)
            .exclude(pk=self.object.pk)
            .order_by("order")
        )
        return context
