from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.industries.models import Industry
from apps.products.models import Product
from apps.services.models import Service


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            "main:home",
            "main:about",
            "products:list",
            "services:list",
            "industries:list",
            "contact:contact",
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(status=Product.STATUS_LIVE)

    def location(self, obj):
        return reverse("products:detail", kwargs={"slug": obj.slug})


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("services:detail", kwargs={"slug": obj.slug})


class IndustrySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Industry.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("industries:detail", kwargs={"slug": obj.slug})
