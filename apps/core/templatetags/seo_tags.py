import json

from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

# Kept in step with the Google Business Profile (Nov 2026). The display text of the
# hours lives in contact/contact.html — change both together.
OPENING_HOURS = [
    (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "08:00", "18:00"),
    (["Saturday"], "08:00", "17:00"),
]
ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "Msakuzi, Ubungo",
    "addressLocality": "Dar es Salaam",
    "postalCode": "16113",
    "addressCountry": "TZ",
}
GEO = {"@type": "GeoCoordinates", "latitude": -6.750417, "longitude": 39.090111}
DESCRIPTION = (
    "IT company in Msakuzi, Ubungo, Dar es Salaam. Custom software and websites, bulk SMS, "
    "mobile money and card payment integrations, managed IT support and consulting. "
    "Products: Smart POS, Smart BMS, PMS and Vikundi."
)


@register.simple_tag(takes_context=True)
def business_jsonld(context) -> str:
    """LocalBusiness structured data so Google can match the site to the BJP Business
    Profile (name, phone, address, hours, logo, social profiles)."""
    company = context["company"]
    base = f"https://{company.domain}"
    same_as = [
        url
        for url in (
            company.instagram_url,
            company.facebook_url,
            company.linkedin_url,
            company.twitter_url,
            company.youtube_url,
        )
        if url
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{base}/#business",
        "name": company.name,
        "url": f"{base}/",
        "logo": base + static("images/logo/bjp-app-icon-512-navy.png"),
        "image": base + static("images/logo/bjp-app-icon-512-navy.png"),
        "description": DESCRIPTION,
        "telephone": company.phone,
        "email": company.email,
        "address": ADDRESS,
        "geo": GEO,
        "hasMap": company.google_maps_url,
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": days,
                "opens": opens,
                "closes": closes,
            }
            for days, opens, closes in OPENING_HOURS
        ],
        "sameAs": same_as,
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')
