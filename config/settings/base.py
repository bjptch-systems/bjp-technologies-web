import os
from pathlib import Path

import pymysql
from django.templatetags.static import static
from django.urls import reverse_lazy
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()

# Django 6 requires mysqlclient >= 2.2.1. PyMySQL reports an older version
# so we patch it here to satisfy the version check.
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.__version__ = "2.2.1"

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]

INSTALLED_APPS = [
    # Unfold must come before django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    # Django built-ins
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Local apps
    "apps.core",
    "apps.main",
    "apps.services",
    "apps.industries",
    "apps.contact",
    "apps.analytics",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.company_info",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASS"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Dar_es_Salaam"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "public" / "static"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "public" / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "BJP Technologies <info@bjptechnologies.co.tz>"
)
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "info@bjptechnologies.co.tz")

# --- Google Analytics Data API (Phase 2 — in-admin dashboard) ---
# The Measurement ID (G-…) for the client-side tag lives in SiteSettings, not here.
# These are the server-side Data API credentials (numeric Property ID + OAuth token).
GA_PROPERTY_ID = os.environ.get("GA_PROPERTY_ID", "")
GA_OAUTH_CLIENT_ID = os.environ.get("GA_OAUTH_CLIENT_ID", "")
GA_OAUTH_CLIENT_SECRET = os.environ.get("GA_OAUTH_CLIENT_SECRET", "")
GA_OAUTH_REFRESH_TOKEN = os.environ.get("GA_OAUTH_REFRESH_TOKEN", "")

# --- Django Unfold Admin ---


def _env_logo(request):
    return static("images/logo/bjp-mark-transparent.png")


UNFOLD = {
    "SITE_TITLE": "BJP Technologies",
    "SITE_HEADER": "BJP Technologies (T) Ltd",
    "SITE_URL": "/",
    "SITE_ICON": _env_logo,
    "SITE_LOGO": _env_logo,
    "SITE_SYMBOL": "shield",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "DASHBOARD_CALLBACK": "apps.core.admin.dashboard_callback",
    "COLORS": {
        "base": {
            "50": "248 250 255",
            "100": "235 240 253",
            "200": "207 220 250",
            "300": "163 191 245",
            "400": "100 144 230",
            "500": "21 101 192",
            "600": "18 82 158",
            "700": "14 62 118",
            "800": "13 27 75",
            "900": "8 15 46",
            "950": "5 9 28",
        },
        "primary": {
            "50": "248 250 255",
            "100": "235 240 253",
            "200": "207 220 250",
            "300": "163 191 245",
            "400": "100 144 230",
            "500": "21 101 192",
            "600": "18 82 158",
            "700": "14 62 118",
            "800": "13 27 75",
            "900": "8 15 46",
            "950": "5 9 28",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {},
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Dashboard",
                "separator": False,
                "items": [
                    {
                        "title": "Overview",
                        "icon": "home",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Website Content",
                "separator": True,
                "items": [
                    {
                        "title": "Services",
                        "icon": "list",
                        "link": reverse_lazy("admin:services_service_changelist"),
                    },
                    {
                        "title": "Industries",
                        "icon": "category",
                        "link": reverse_lazy("admin:industries_industry_changelist"),
                    },
                ],
            },
            {
                "title": "Site Settings",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Logo & Branding",
                        "icon": "image",
                        "link": reverse_lazy("admin:core_logobrandingsettings_changelist"),
                    },
                    {
                        "title": "Company Identity",
                        "icon": "business",
                        "link": reverse_lazy("admin:core_companyidentitysettings_changelist"),
                    },
                    {
                        "title": "Address",
                        "icon": "location_on",
                        "link": reverse_lazy("admin:core_addresssettings_changelist"),
                    },
                    {
                        "title": "Social Media",
                        "icon": "share",
                        "link": reverse_lazy("admin:core_socialmediasettings_changelist"),
                    },
                    {
                        "title": "Hero Section",
                        "icon": "web_asset",
                        "link": reverse_lazy("admin:core_herosectionsettings_changelist"),
                    },
                    {
                        "title": "Stats Counters",
                        "icon": "bar_chart",
                        "link": reverse_lazy("admin:core_statscounterssettings_changelist"),
                    },
                    {
                        "title": "About Strip",
                        "icon": "info",
                        "link": reverse_lazy("admin:core_aboutstripsettings_changelist"),
                    },
                    {
                        "title": "About Page",
                        "icon": "person",
                        "link": reverse_lazy("admin:core_aboutpagesettings_changelist"),
                    },
                    {
                        "title": "Services Page",
                        "icon": "build",
                        "link": reverse_lazy("admin:core_servicespagesettings_changelist"),
                    },
                    {
                        "title": "Industries Page",
                        "icon": "factory",
                        "link": reverse_lazy("admin:core_industriespagesettings_changelist"),
                    },
                    {
                        "title": "Contact Page",
                        "icon": "map",
                        "link": reverse_lazy("admin:core_contactpagesettings_changelist"),
                    },
                    {
                        "title": "Footer CTA",
                        "icon": "campaign",
                        "link": reverse_lazy("admin:core_footerctasettings_changelist"),
                    },
                ],
            },
            {
                "title": "Enquiries",
                "separator": True,
                "items": [
                    {
                        "title": "Contact Enquiries",
                        "icon": "mail",
                        "link": reverse_lazy("admin:contact_contactenquiry_changelist"),
                        "badge": "apps.core.admin.enquiry_badge",
                    },
                ],
            },
            {
                "title": "Analytics",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Overview",
                        "icon": "insights",
                        "link": reverse_lazy("admin:analytics_analyticsoverview_changelist"),
                    },
                    {
                        "title": "Google Analytics",
                        "icon": "analytics",
                        "link": reverse_lazy("admin:core_analyticssettings_changelist"),
                    },
                ],
            },
            {
                "title": "Administration",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
        ],
    },
}
