from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.core.sitemaps import (
    IndustrySitemap,
    ProductSitemap,
    ServiceSitemap,
    StaticViewSitemap,
)
from apps.core.webhook import github_webhook

sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
    "services": ServiceSitemap,
    "industries": IndustrySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path(
        "sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"
    ),
    path("", include("apps.main.urls", namespace="main")),
    path("products/", include("apps.products.urls", namespace="products")),
    path("services/", include("apps.services.urls", namespace="services")),
    path("industries/", include("apps.industries.urls", namespace="industries")),
    path("contact/", include("apps.contact.urls", namespace="contact")),
    path("deploy/webhook/", github_webhook, name="github_webhook"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
