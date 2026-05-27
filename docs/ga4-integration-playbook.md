# GA4 Integration Playbook — Django + Unfold

> A portable, step-by-step reference for adding **Google Analytics 4** to any Django
> site and surfacing the traffic data **inside the Django admin** as a styled dashboard.
> Distilled from the Bejundas Platform build. Copy this into a new project, run a
> find-and-replace on the IDs (see §11), and you have analytics end to end.

**What you get when you finish:**

1. **Client-side tracking** — the gtag.js tag on every public page, editable + kill-switchable from admin, automatically suppressed in local dev.
2. **Conversion tracking** — named events fired on form submissions (contact, orders, quotes, leads…).
3. **An in-admin dashboard** — realtime active users, traffic over time, top pages, sources, countries, device split, and conversion counts — rendered inside the admin chrome (Unfold sidebar, dark mode, breadcrumbs all intact), with caching so you never blow the API quota.

The work splits into two phases that ship independently:

- **Phase 1 — the tag.** Ship first. Starts collecting data immediately. No Google Cloud project needed.
- **Phase 2 — the dashboard.** Needs a Google Cloud project + OAuth, and needs ~48h of collected data before standard reports return non-zero numbers.

---

## Table of contents

- [0. Concepts you must not confuse](#0-concepts-you-must-not-confuse)
- [1. Prerequisites](#1-prerequisites)
- [2. Google setup (console clicks)](#2-google-setup-console-clicks)
- [3. Phase 1 — the tracking tag](#3-phase-1--the-tracking-tag)
- [4. Conversion events](#4-conversion-events)
- [5. Phase 2 — Google Cloud + OAuth](#5-phase-2--google-cloud--oauth)
- [6. Phase 2 — the data service layer](#6-phase-2--the-data-service-layer)
- [7. Phase 2 — mounting the dashboard inside admin](#7-phase-2--mounting-the-dashboard-inside-admin)
- [8. Phase 2 — the dashboard UI (the important part)](#8-phase-2--the-dashboard-ui-the-important-part)
- [9. Tests](#9-tests)
- [10. Deploy checklist](#10-deploy-checklist)
- [11. Adapting this to a new site](#11-adapting-this-to-a-new-site)
- [12. Failure modes](#12-failure-modes)

---

## 0. Concepts you must not confuse

| Thing | Looks like | Used by | Where it lives |
|---|---|---|---|
| **Measurement ID** | `G-XXXXXXXXXX` | the gtag.js **tag** (client side) | rendered into every page's `<head>` |
| **Property ID** | `538542797` (numeric) | the GA4 **Data API** (server side) | env var, used in report queries |
| **Stream ID** | `14922032581` (numeric) | informational | GA4 console only |

The Measurement ID and the Property ID are **not interchangeable**. The tag uses the
`G-` one; the dashboard's API calls use the numeric one. Mixing them up is the single
most common mistake — symptoms are "tag works but dashboard 404s the property" or vice versa.

**Two auth models for the Data API — pick OAuth user-token, not a service account, if you're on a personal Gmail.**
A service account is the "correct" way, but GA4 refuses to attach a service-account
email to a property owned by a personal Gmail account ("doesn't match a Google Account"),
and the API fallback needs a restricted scope Google blocks for personal accounts. The
working path for solo/personal-account projects is: authenticate **as yourself** (you're
already a GA4 admin) via a Desktop OAuth client, capture a refresh token once, store it in
env. That's what this playbook uses. If your GA4 property is owned by a **Google Workspace**
org, a service account is cleaner — but the dashboard code is identical either way; only
`_credentials()` changes.

---

## 1. Prerequisites

- A Django project (4.2+ / 5.x). This guide assumes `django-unfold` for admin theming. If you use vanilla admin, the dashboard still works — you just extend `admin/base_site.html` instead of `unfold/layouts/base_simple.html` and skip the sidebar-config step.
- A `SiteSettings` singleton model (or any place to store an editable Measurement ID). If you don't have one, you can hardcode the ID in `settings.py` instead — §3 covers both.
- A Django cache backend configured (LocMemCache is fine for a single process; use Redis/Memcached if you run multiple workers, so the cache is shared).
- A Google account that is an **Administrator** on the GA4 property.

---

## 2. Google setup (console clicks)

Do this once per site.

### 2.1 Create the GA4 property + data stream

1. <https://analytics.google.com> → **Admin** (gear) → **Create → Property**.
2. Name it, set timezone + currency → **Next** → fill business details → **Create**.
3. **Data Streams → Add stream → Web.** Enter the site URL + a stream name → **Create stream.**
4. The stream panel shows your **Measurement ID** `G-XXXXXXXXXX`. Copy it. (This is for Phase 1.)
5. Note the **Property ID** (numeric) — **Admin → Property Settings**, top right. Copy it. (This is for Phase 2.)

That's all you need for Phase 1. You can ship the tag now and come back for Phase 2.

---

## 3. Phase 1 — the tracking tag

### 3.1 Store the Measurement ID (editable from admin)

Add two fields to your `SiteSettings` singleton — the ID and a master kill switch:

```python
# apps/core/models.py  (inside SiteSettings)
ga_measurement_id = models.CharField(
    max_length=20,
    blank=True,
    default="",
    help_text="GA4 Measurement ID (starts with G-). Leave blank to disable tracking.",
)
ga_enabled = models.BooleanField(
    default=True,
    help_text="Master switch — uncheck to disable analytics site-wide without removing the ID.",
)
```

```bash
python manage.py makemigrations
python manage.py migrate
```

**Optional but recommended — seed the ID via a data migration** so production picks it up
on first deploy without anyone touching the admin:

```python
# apps/core/migrations/000X_seed_ga_measurement_id.py
from django.db import migrations

GA_MEASUREMENT_ID = "G-XXXXXXXXXX"  # your ID

def seed(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(
        pk="00000000-0000-0000-0000-000000000001"
    )
    if not obj.ga_measurement_id:
        obj.ga_measurement_id = GA_MEASUREMENT_ID
        obj.save(update_fields=["ga_measurement_id"])

class Migration(migrations.Migration):
    dependencies = [("core", "000X_analytics_fields")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
```

> No `SiteSettings`? Skip the model fields and just put `GA_MEASUREMENT_ID = env("GA_MEASUREMENT_ID", default="")` in `settings.py`, then reference `settings.GA_MEASUREMENT_ID` in the template via a context processor. Everything else is the same.

### 3.2 Expose it to templates via a context processor

The key trick: **only emit the tag when it's safe and wanted.** That means
`not DEBUG` (so local dev never pollutes production stats) **and** the switch is on
**and** an ID exists:

```python
# apps/core/context_processors.py
from django.conf import settings
from apps.core.models import SiteSettings

def company_info(request):
    company = SiteSettings.get()
    return {
        "company": company,
        "analytics_enabled": (
            not settings.DEBUG
            and company.ga_enabled
            and bool(company.ga_measurement_id)
        ),
    }
```

Register it:

```python
# settings.py → TEMPLATES → OPTIONS → context_processors
"apps.core.context_processors.company_info",
```

### 3.3 Render the tag in your base template

In the site-wide base template's `<head>`:

```django
{% if analytics_enabled %}
<!-- Google tag (gtag.js) — GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ company.ga_measurement_id }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ company.ga_measurement_id }}');
</script>
{% endif %}
```

### 3.4 Add an admin entry to edit it

If you use the singleton + proxy-admin pattern, add a proxy model and register it so
"Google Analytics" shows up as its own sidebar entry:

```python
# models.py
class AnalyticsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Google Analytics"
        verbose_name_plural = "Google Analytics"

# admin.py  (_BaseSiteSettingsAdmin redirects changelist → the singleton change form)
@admin.register(AnalyticsSettings)
class AnalyticsSettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        ("Google Analytics (GA4)", {
            "fields": ("ga_measurement_id", "ga_enabled"),
            "description": "GA4 tag injected on every public page when enabled. "
                           "Suppressed automatically when DEBUG is on.",
        }),
    )
```

### 3.5 Verify Phase 1

The tag never renders in DEBUG, so to test the *rendering* locally:

```bash
DEBUG=False python manage.py runserver
```

Then **view-source** any public page and search for your `G-` ID. After deploy:

1. Open the live site in incognito.
2. GA4 → **Reports → Realtime** → you should appear within ~30s.

---

## 4. Conversion events

A conversion = a meaningful action, almost always a form submission. The pattern: the
view passes a `ga_event` name into the success-render context; the base template fires it.

### 4.1 The event block in the base template

Put this **just before `</body>`** (after gtag.js has loaded):

```django
{% if analytics_enabled and ga_event %}
<script>
  if (typeof gtag === 'function') {
    gtag('event', '{{ ga_event|escapejs }}'{% if ga_event_params %}, {{ ga_event_params|safe }}{% endif %});
  }
</script>
{% endif %}
```

### 4.2 Fire it from a view

On the **success path only** (after the form validates and saves), add `ga_event` to the
context. Optionally pass params as a JSON string:

```python
# simple case
return render(request, "hub/contact.html",
              {"form": ContactForm(), "sent": True, "ga_event": "contact_submit"})

# with params
import json
return render(request, "leads/coming_soon.html", {
    "form": LeadForm(), "submitted": True,
    "ga_event": "lead_submit",
    "ga_event_params": json.dumps({"vertical": vertical}),
})
```

### 4.3 Keep a canonical list of event names

Decide your event names up front and keep them in **one place** (you'll reference them
again in the dashboard's conversion card). Example set:

| Event name | Fires when |
|---|---|
| `contact_submit` | any contact form |
| `lead_submit` | coming-soon / newsletter capture |
| `order_inquiry_submit` | product order inquiry |
| `quote_request_submit` | quote request |
| `loan_inquiry_submit` | loan application |
| `investment_inquiry_submit` | investment inquiry |

### 4.4 Mark them as Key Events in GA4

Once the events are flowing (check Realtime), go to **GA4 → Admin → Events** and toggle
each one as a **Key Event** (the GA4 term for "conversion"). Also add an **Internal traffic
data filter** (Admin → Data Settings → Data Filters) that excludes your office IP, and set
it Active.

---

## 5. Phase 2 — Google Cloud + OAuth

This is the part that lets the server *read* analytics back. Phase 1 only *sends* data.

### 5.1 Python packages

```text
# requirements.txt
google-analytics-data>=0.18,<1.0
google-auth>=2.30,<3.0
google-auth-oauthlib>=1.2,<2.0
```

### 5.2 Create the GCP project + enable the API

1. <https://console.cloud.google.com> → create a project (e.g. `mysite-analytics`).
2. **APIs & Services → Library** → search **"Google Analytics Data API"** → **Enable**.

### 5.3 OAuth consent screen

1. **APIs & Services → OAuth consent screen.**
2. User type **External** → fill app name, support email, developer email → save.
3. **Scopes** step: you don't strictly need to add scopes here (the capture script
   requests `analytics.readonly` directly), but adding it is harmless.
4. **Test users**: add your own Google account while in Testing mode.
5. **PUBLISH THE APP.** Status must read **"In production"**, not "Testing".
   This is critical: **Testing-mode refresh tokens expire after 7 days.** Published
   tokens are permanent (the only remaining killer is 6 months unused — your dashboard's
   constant polling prevents that). You do **not** need full app verification — the
   "unverified app" warning is harmless for a single-user internal tool. Publishing alone
   stops the 7-day expiry.

### 5.4 Create the Desktop OAuth client

1. **APIs & Services → Credentials → Create Credentials → OAuth client ID.**
2. Application type: **Desktop app** → name it → **Create**.
3. **Download JSON.** This file has `client_id` + `client_secret`. Keep it out of git.

### 5.5 Capture the refresh token (one-time)

Add this management command, then run it once locally:

```python
# apps/core/management/commands/ga_capture_token.py
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

class Command(BaseCommand):
    help = "Capture a GA4 Data API refresh token via OAuth flow (one-time setup)."

    def add_arguments(self, parser):
        parser.add_argument("client_secrets_file", type=str,
                            help="Path to the OAuth client JSON from GCP Console.")

    def handle(self, *args, **options):
        from google_auth_oauthlib.flow import InstalledAppFlow

        path = Path(options["client_secrets_file"]).expanduser()
        if not path.exists():
            raise CommandError(f"Client secrets file not found: {path}")
        with open(path) as f:
            config = json.load(f)
        installed = config.get("installed") or config.get("web")
        if not installed:
            raise CommandError("Not an OAuth client JSON (expected 'installed'/'web' key). "
                               "Did you download a service-account key by mistake?")
        client_id = installed["client_id"]
        client_secret = installed["client_secret"]

        flow = InstalledAppFlow.from_client_secrets_file(str(path), scopes=SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True, prompt="consent")
        if not creds.refresh_token:
            raise CommandError(
                "No refresh token returned. Revoke prior consent at "
                "https://myaccount.google.com/permissions and retry — Google only "
                "issues a refresh token on first consent."
            )

        self.stdout.write(self.style.SUCCESS("✓ OAuth complete. Paste into .env:\n"))
        self.stdout.write(f"GA_OAUTH_CLIENT_ID={client_id}")
        self.stdout.write(f"GA_OAUTH_CLIENT_SECRET={client_secret}")
        self.stdout.write(f"GA_OAUTH_REFRESH_TOKEN={creds.refresh_token}")
        self.stdout.write("GA_PROPERTY_ID=<your-numeric-property-id>")
        self.stdout.write("\nDO NOT commit .env.")
```

```bash
python manage.py ga_capture_token /path/to/oauth-client.json
```

A browser opens. Log in with the **GA4 admin** account. You'll hit a
**"Google hasn't verified this app"** screen → **Advanced → Go to {app} (unsafe)** →
grant access. The command prints four `GA_*` lines.

### 5.6 Env vars

```text
# .env  (and .env.example with blank values)
GA_PROPERTY_ID=538542797
GA_OAUTH_CLIENT_ID=...apps.googleusercontent.com
GA_OAUTH_CLIENT_SECRET=GOCSPX-...
GA_OAUTH_REFRESH_TOKEN=1//03...
```

```python
# settings.py
GA_PROPERTY_ID         = env("GA_PROPERTY_ID", default="")
GA_OAUTH_CLIENT_ID     = env("GA_OAUTH_CLIENT_ID", default="")
GA_OAUTH_CLIENT_SECRET = env("GA_OAUTH_CLIENT_SECRET", default="")
GA_OAUTH_REFRESH_TOKEN = env("GA_OAUTH_REFRESH_TOKEN", default="")
```

> **Security:** the refresh token grants read access to your analytics account.
> Never commit it. On a public repo a leak is permanent — rotate immediately (regenerate
> in GCP + revoke at <https://myaccount.google.com/permissions>) if it ever lands in git
> or chat.

### 5.7 Verify the credentials

Add a smoke-test command (full version in the Bejundas repo at
`apps/core/management/commands/ga_verify.py`) — the core of it:

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest
from google.oauth2.credentials import Credentials

creds = Credentials(
    token=None,
    refresh_token=settings.GA_OAUTH_REFRESH_TOKEN,
    client_id=settings.GA_OAUTH_CLIENT_ID,
    client_secret=settings.GA_OAUTH_CLIENT_SECRET,
    token_uri="https://oauth2.googleapis.com/token",
    scopes=["https://www.googleapis.com/auth/analytics.readonly"],
)
client = BetaAnalyticsDataClient(credentials=creds)
resp = client.run_report(RunReportRequest(
    property=f"properties/{settings.GA_PROPERTY_ID}",
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    metrics=[Metric(name="activeUsers"), Metric(name="screenPageViews")],
))
```

```bash
python manage.py ga_verify
```

Zero values are fine if the property is < 48h old — it confirms auth works, there's
just nothing to report yet.

---

## 6. Phase 2 — the data service layer

Create `apps/analytics/`. **All Data API calls go through one module** so there's a
single place that builds credentials, caches responses, and returns typed rows. This
matters because the **Data API has a ~25,000 token/day quota per property** — uncached
calls on every admin page view would exhaust it in hours.

### 6.1 `services.py` — the shape

```python
from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass
from django.conf import settings
from django.core.cache import cache


def _credentials():
    from google.oauth2.credentials import Credentials
    return Credentials(
        token=None,
        refresh_token=settings.GA_OAUTH_REFRESH_TOKEN,
        client_id=settings.GA_OAUTH_CLIENT_ID,
        client_secret=settings.GA_OAUTH_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )

def _client():
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    return BetaAnalyticsDataClient(credentials=_credentials())

def is_configured() -> bool:
    """View code checks this so a missing-env-var deploy shows a friendly
    page instead of a 500."""
    return bool(
        settings.GA_PROPERTY_ID and settings.GA_OAUTH_CLIENT_ID
        and settings.GA_OAUTH_CLIENT_SECRET and settings.GA_OAUTH_REFRESH_TOKEN
    )

def _property() -> str:
    return f"properties/{settings.GA_PROPERTY_ID}"
```

### 6.2 The cached report runner

Both standard and realtime reports go through cached wrappers. Note the
`bypass_cache` flag — that's what the dashboard's "Refresh" button uses.

```python
def _run_report_cached(cache_key, ttl, *, metrics, dimensions=(),
                       start="7daysAgo", end="today", limit=None, bypass_cache=False):
    cached = None if bypass_cache else cache.get(cache_key)
    if cached is not None:
        return cached

    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest)
    request = RunReportRequest(
        property=_property(),
        date_ranges=[DateRange(start_date=start, end_date=end)],
        metrics=[Metric(name=m) for m in metrics],
        dimensions=[Dimension(name=d) for d in dimensions],
        limit=limit or 10000,
    )
    response = _client().run_report(request)
    payload = {
        "rows": [
            {"dimensions": [v.value for v in row.dimension_values],
             "metrics":    [v.value for v in row.metric_values]}
            for row in response.rows
        ],
        "totals": [[v.value for v in t.metric_values] for t in (response.totals or [])],
    }
    cache.set(cache_key, payload, ttl)
    return payload


def _run_realtime_cached(cache_key, ttl, *, bypass_cache=False) -> int:
    cached = None if bypass_cache else cache.get(cache_key)
    if cached is not None:
        return cached
    from google.analytics.data_v1beta.types import Metric, RunRealtimeReportRequest
    response = _client().run_realtime_report(
        RunRealtimeReportRequest(property=_property(), metrics=[Metric(name="activeUsers")]))
    value = int(response.rows[0].metric_values[0].value) if response.rows else 0
    cache.set(cache_key, value, ttl)
    return value
```

> **The `rows[0]` gotcha that cost real debugging time.** When you request metrics with
> **no dimensions**, the API returns a **single row** whose metric values *are* the totals
> for the date range. `response.totals[]` stays **empty** unless you explicitly set
> `metric_aggregations` on the request. So read headline numbers from `rows[0]`, **not**
> `totals[0]` — otherwise every KPI shows 0 even though the data is there.

### 6.3 Typed helpers + cache TTLs

Wrap each report in a small typed helper returning frozen dataclasses (cleaner templates,
testable shapes). Recommended TTLs balance "feels live" against quota:

| Helper | Metrics / dimensions | TTL |
|---|---|---|
| `realtime_active_users()` | `activeUsers` (realtime) | **60s** |
| `headline_kpis()` | `activeUsers`, `screenPageViews` × today/7d/30d | **30 min** |
| `top_pages(limit=5)` | `screenPageViews` by `pagePath`, `pageTitle` (7d) | **1 hr** |
| `top_sources(limit=5)` | `sessions` by `sessionSource` (7d) | **1 hr** |
| `top_countries(limit=5)` | `activeUsers` by `country` (30d) | **1 hr** |
| `device_breakdown()` | `activeUsers` by `deviceCategory` (30d) | **1 hr** |
| `conversions_30d()` | `eventCount` by `eventName` (30d) | **30 min** |

Example helper (the headline one, showing the `rows[0]` handling):

```python
@dataclass(frozen=True)
class Kpi:
    label: str; value: int; window: str

def headline_kpis(*, bypass_cache=False) -> list[Kpi]:
    out = []
    for lu, lv, start, window in (
        ("Users (Today)", "Page Views (Today)", "today", "today"),
        ("Users (7d)", "Page Views (7d)", "7daysAgo", "last 7 days"),
        ("Users (30d)", "Page Views (30d)", "30daysAgo", "last 30 days"),
    ):
        p = _run_report_cached(f"ga:headline:{start}", ttl=1800,
                               metrics=["activeUsers", "screenPageViews"],
                               start=start, end="today", bypass_cache=bypass_cache)
        row = p["rows"][0]["metrics"] if p["rows"] else (p["totals"][0] if p["totals"] else ["0","0"])
        out.append(Kpi(label=lu, value=int(row[0] or 0), window=window))
        out.append(Kpi(label=lv, value=int(row[1] or 0), window=window))
    return out
```

### 6.4 Conversion events — map names to friendly labels/icons

Keep this in sync with the event names you fired in §4:

```python
CONVERSION_EVENT_NAMES = (
    "lead_submit", "contact_submit", "order_inquiry_submit",
    "quote_request_submit", "loan_inquiry_submit", "investment_inquiry_submit",
)
CONVERSION_EVENT_LABELS = {"lead_submit": "Coming Soon Lead", "contact_submit": "Contact Form", ...}
CONVERSION_EVENT_ICONS  = {"lead_submit": "person_add",       "contact_submit": "mail", ...}

@dataclass(frozen=True)
class ConversionRow:
    event_name: str; count: int
    @property
    def label(self): return CONVERSION_EVENT_LABELS.get(self.event_name, self.event_name)
    @property
    def icon(self):  return CONVERSION_EVENT_ICONS.get(self.event_name, "bolt")

def conversions_30d(*, bypass_cache=False) -> list[ConversionRow]:
    p = _run_report_cached("ga:conversions:30d", ttl=1800, metrics=["eventCount"],
                           dimensions=["eventName"], start="30daysAgo", end="today",
                           bypass_cache=bypass_cache)
    by_name = {r["dimensions"][0]: int(r["metrics"][0] or 0) for r in p["rows"]}
    # iterate over OUR canonical list so events with zero count still render a card
    return [ConversionRow(event_name=n, count=by_name.get(n, 0)) for n in CONVERSION_EVENT_NAMES]
```

### 6.5 Cache-busting for the Refresh button

```python
def invalidate_all():
    cache.delete_many([
        "ga:realtime:active", "ga:headline:today", "ga:headline:7daysAgo",
        "ga:headline:30daysAgo", "ga:top_pages:7d:5", "ga:top_sources:7d:5",
        "ga:top_countries:30d:5", "ga:devices:30d", "ga:conversions:30d",
    ])
```

---

## 7. Phase 2 — mounting the dashboard inside admin

**The goal:** a custom page that lives inside admin so it inherits the Unfold sidebar,
header, breadcrumbs and dark-mode toggle automatically. The clean way to do this is **not**
a standalone URL — that page would have no admin chrome because Django only builds the
chrome context (`admin_site.each_context(request)`) for requests routed through the admin.

**The trick: a virtual model + a `ModelAdmin` whose `changelist_view` renders the dashboard.**

### 7.1 The virtual model

```python
# apps/analytics/models.py
from django.db import models

class AnalyticsOverview(models.Model):
    """Virtual entry point. The table is created empty and never written to;
    it exists only to give admin a URL to hand off to."""
    class Meta:
        verbose_name = "Overview"
        verbose_name_plural = "Overview"
        default_permissions = ()   # don't generate add/change/delete/view perms

    def __str__(self):  # pragma: no cover
        return "Analytics Overview"
```

```bash
python manage.py makemigrations analytics && python manage.py migrate
```

### 7.2 The admin that renders the dashboard

```python
# apps/analytics/admin.py
import logging
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from unfold.admin import ModelAdmin
from apps.analytics import services
from apps.analytics.models import AnalyticsOverview

logger = logging.getLogger(__name__)

@admin.register(AnalyticsOverview)
class AnalyticsOverviewAdmin(ModelAdmin):
    def has_add_permission(self, request):    return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False
    def has_view_permission(self, request, obj=None):
        return bool(request.user and request.user.is_staff)

    def changelist_view(self, request, extra_context=None):
        base_ctx = self.admin_site.each_context(request)   # ← the chrome

        if not services.is_configured():
            return TemplateResponse(request, "admin/analytics/not_configured.html",
                                    {**base_ctx, "title": "Analytics — Setup Required"})

        if request.GET.get("refresh") == "1":
            services.invalidate_all()
            return redirect(request.path)

        ctx = _build_dashboard_context()
        ctx.update(base_ctx)
        ctx["title"] = "Analytics — Overview"
        if extra_context:
            ctx.update(extra_context)
        return TemplateResponse(request, "admin/analytics/overview.html", ctx)
```

`_build_dashboard_context()` calls each service helper inside one `try/except` (so one
failing report surfaces an error banner instead of a 500), computes `max_*` values for bar
widths, and returns a flat dict. Keep it as a **module-level function**, separate from the
admin class, so tests can call it directly with `services` mocked.

> **Why `each_context` is the whole game:** that one call is the source of `available_apps`
> (the sidebar), `site_header`, the dark-mode state, etc. Merge it into your context and the
> page looks native. Forget it and you get an unstyled orphan page floating in the void —
> which is exactly the bug that wasted an afternoon on the original build. Add a regression
> test asserting `available_apps` and `site_header` are in the response context.

### 7.3 Sidebar entry (Unfold)

```python
# settings.py → UNFOLD["SIDEBAR"]["navigation"]
{
    "title": "Analytics",
    "separator": True,
    "collapsible": True,
    "items": [
        {"title": "Google Analytics", "icon": "analytics",
         "link": reverse_lazy("admin:core_analyticssettings_changelist")},   # the tag settings
        {"title": "Overview", "icon": "insights",
         "link": reverse_lazy("admin:analytics_analyticsoverview_changelist")},  # the dashboard
    ],
},
```

The admin URL name follows the pattern `admin:<app_label>_<model_name>_changelist`, i.e.
`admin:analytics_analyticsoverview_changelist`.

---

## 8. Phase 2 — the dashboard UI (the important part)

You asked for the UI specifically, so read this section carefully — it contains the one
non-obvious thing that breaks every first attempt.

### 8.1 The Unfold-Tailwind trap

Unfold ships a **precompiled, NARROW Tailwind bundle** — it contains **only the utility
classes Unfold's own templates use.** So when you write a dashboard with `text-7xl`,
`bg-emerald-500`, `rounded-2xl`, gradients, `shadow-lg`, arbitrary values like `text-[11px]`
— **most of them silently do nothing.** No error. The class is just absent from the CSS, so
the element renders unstyled. The page looks broken and you can't see why in the markup.

This is *not* a bug you debug by re-reading your HTML. Confirm it with the browser:
`getComputedStyle($0)` on an element shows the property never applied. (Use the
`webapp-testing` Playwright skill / browser devtools — don't guess.)

### 8.2 The fix: ship your own scoped CSS

Define **every** utility the dashboard needs as raw CSS, scoped under one wrapper class
(`.ga-dash`) so it can't leak into the rest of admin. Put it in the template's
`{% block extrastyle %}`. Then wrap the whole dashboard in `<div class="ga-dash">`.

```django
{% extends "unfold/layouts/base_simple.html" %}
{% block breadcrumbs %}{% endblock %}
{% block extrastyle %}{{ block.super }}
<style>
  /* Typography — Unfold's bundle lacks the big sizes */
  .ga-dash .text-3xl { font-size: 1.875rem !important; line-height: 1 !important; }
  .ga-dash .text-6xl { font-size: 3.75rem  !important; line-height: 1 !important; }
  .ga-dash .text-7xl { font-size: 4.5rem   !important; line-height: 1 !important; }
  .ga-dash .font-black { font-weight: 900 !important; }
  .ga-dash .tabular-nums { font-variant-numeric: tabular-nums !important; }
  .ga-dash .text-\[11px\] { font-size: 11px !important; }   /* escape arbitrary values */

  /* Color palette — emerald/amber/rose/blue aren't in the bundle */
  .ga-dash .bg-emerald-500 { background-color: #10b981 !important; }
  .ga-dash .text-blue-600  { color: #2563eb !important; }
  /* …repeat for each color you actually use… */

  /* Rounded + shadows */
  .ga-dash .rounded-2xl { border-radius: 16px !important; }
  .ga-dash .shadow-lg   { box-shadow: 0 10px 25px -5px rgba(0,0,0,.15) !important; }

  /* Semantic component classes — cleaner than utility soup */
  .ga-card { background:#fff; border:1px solid #f3f4f6; border-radius:16px;
             box-shadow:0 1px 3px rgba(0,0,0,.06); transition:transform .15s, box-shadow .15s; }
  .ga-card:hover { transform: translateY(-2px); }

  /* Hero (gradient) cards need a SEPARATE class — .ga-card's white bg would
     override the gradient otherwise. This was a real bug. */
  .ga-card-hero { border:none; border-radius:16px; color:#fff;
                  box-shadow:0 10px 25px -5px rgba(0,0,0,.15); overflow:hidden; position:relative; }
  .ga-card-hero.ga-grad-primary { background: linear-gradient(135deg,#1a1a2e 0%,#2563eb 100%); }
  .ga-card-hero.ga-grad-emerald { background: linear-gradient(135deg,#064e3b 0%,#10b981 100%); }

  /* Progress bars */
  .ga-bar-track { height:6px; background:#f3f4f6; border-radius:9999px; overflow:hidden; }
  .ga-bar-fill  { height:100%; border-radius:9999px; transition:width .6s cubic-bezier(.2,.8,.2,1); }

  /* Pulsing "live" dot */
  @keyframes ga-ping { 0%{transform:scale(1);opacity:.75} 75%,100%{transform:scale(2.4);opacity:0} }
  .ga-dash .ga-pulse-ring { animation: ga-ping 1.4s cubic-bezier(0,0,.2,1) infinite; }

  /* Dark mode — Unfold toggles .dark on <html> */
  html.dark .ga-card { background:#111827; border-color:#1f2937; }
  html.dark .ga-bar-track { background:#1f2937; }
</style>
{% endblock %}

{% block content %}
<div class="ga-dash px-4 sm:px-6 lg:px-8 py-6 space-y-8 max-w-[1400px] mx-auto">
  ...
</div>
{% endblock %}
```

> The full, copy-pasteable version (every color, every helper, all dark-mode overrides) is
> in the Bejundas repo at `apps/analytics/templates/admin/analytics/overview.html` — lift it
> wholesale and trim to the classes you use.

### 8.3 Layout structure

The dashboard is plain CSS grid + the cards above:

1. **Header row** — title + the `?refresh=1` "Refresh data" button.
2. **Error banner** — `{% if error %}` shows the exception verbatim (incl. the "token may
   have expired" hint).
3. **Hero row** (3-col grid) — big **realtime active users** card (2 cols, with the pulsing
   dot) + **total conversions** card.
4. **Traffic-over-time** — 3 KPI cards (today / 7d / 30d), each split Users | Page views.
5. **Top pages + Traffic sources** (2-col) — bars sized with `{% widthratio row.views max_views 100 %}`.
6. **Countries + Devices** (2-col) — countries as bars; devices as one stacked bar + a legend.
7. **Conversion events** — 6-up grid of count cards, "live" badge when count > 0.

### 8.4 Two template gotchas

- **Bar widths:** use `{% widthratio current max 100 %}` for the percentage. Always guard
  `max` to be ≥ 1 in the context builder (`max(... , default=1) or 1`) or you divide by zero.
- **Per-segment colors that must survive the narrow bundle:** for the stacked device bar,
  set colors **inline** via `{% cycle '#10b981' '#3b82f6' '#f59e0b' '#f43f5e' as device_color %}`,
  and `{% resetcycle device_color %}` before the legend so the legend dots match the bar.
  Inline styles always render; utility classes might not.

### 8.5 The not-configured fallback

Render `admin/analytics/not_configured.html` (also extending `unfold/layouts/base_simple.html`)
when `services.is_configured()` is False — list the four missing env vars and the
`ga_capture_token` / `ga_verify` commands. This turns a misconfigured deploy into a helpful
page instead of a 500.

---

## 9. Tests

Mock `services` — never hit the real API in tests. Patch at the point of use
(`apps.analytics.admin.services`). Cover:

- **Context builder** (`_build_dashboard_context`) with `services` mocked → asserts the dict shape and the `max_*` math.
- **`headline_kpis` regression** → feed a payload with `rows` set + `totals` empty, assert KPIs are non-zero (guards the `rows[0]` gotcha).
- **Admin view** → `admin:analytics_analyticsoverview_changelist` returns 200, uses the right template, and (regression) **`available_apps` + `site_header` are in `response.context`** (guards the missing-chrome bug).
- **not_configured path** → with env vars blank, the setup template renders.
- **Permissions** → non-staff gets denied.

```bash
pytest apps/analytics
ruff check . && black --check .
```

---

## 10. Deploy checklist

- [ ] `requirements.txt` has the three Google packages; rebuild the server venv.
- [ ] Add the four `GA_*` env vars on the server (cPanel: **Setup Python App → Environment variables**).
- [ ] `python manage.py migrate` (analytics table + the seed migration).
- [ ] Confirm `DEBUG=False` in production (else the tag never renders).
- [ ] Visit the live site in incognito → view-source → `G-` ID present.
- [ ] GA4 → Realtime → you appear.
- [ ] Open `/admin/` → Analytics → Overview → dashboard renders with real numbers.
- [ ] **OAuth consent screen is "In production"** (not Testing) so the token never expires.
- [ ] GA4 → mark the conversion events as Key Events; add the internal-traffic filter.
- [ ] (GA4 → Admin → Data Settings → Data Retention → set to **14 months**.)

---

## 11. Adapting this to a new site

Find-and-replace these when you copy the code across:

| Placeholder | Replace with |
|---|---|
| `G-XXXXXXXXXX` | the new site's Measurement ID |
| `538542797` | the new site's numeric Property ID |
| `apps.core` / `SiteSettings` | your settings model's app + name (or use a plain `settings.py` constant) |
| `00000000-…-001` | your singleton's PK (or drop the seed migration and set the ID in admin) |
| `CONVERSION_EVENT_*` dicts + view `ga_event` names | the new site's actual forms/events |
| `unfold/layouts/base_simple.html` | `admin/base_site.html` if not using Unfold |
| brand gradient colors in `.ga-card-hero` | the new site's palette |

**What stays identical:** `services.py` plumbing, the `_run_report_cached` /
`_run_realtime_cached` pattern, the `rows[0]` handling, the virtual-model + `changelist_view`
trick, the `each_context` merge, the scoped-CSS approach to the Unfold-Tailwind trap, and the
OAuth capture/verify commands. That's ~80% of the work and it's fully portable.

---

## 12. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Tag missing from page source | `DEBUG=True` in prod, `ga_enabled=False`, or blank `ga_measurement_id` | Check `.env` + admin |
| Every KPI shows 0 but Realtime works | reading `response.totals[]` (empty without `metric_aggregations`) | Read `rows[0]` instead (§6.2) |
| Dashboard styling looks broken / huge plain text | Unfold's narrow Tailwind bundle dropped your classes | Ship scoped CSS under `.ga-dash` (§8.2) |
| Hero cards lost their gradient | `.ga-card`'s white background overrode the gradient | Use a separate `.ga-card-hero` class (§8.2) |
| Dashboard page has no sidebar / unstyled | `each_context()` not merged, or page mounted outside admin URLs | Use the virtual-model trick; merge `each_context` (§7.2) |
| `invalid_grant` after ~7 days | OAuth app still in "Testing" mode | Publish the consent screen to production (§5.3), re-capture token |
| 403 `PERMISSION_DENIED` on the property | auth account isn't a GA4 admin/viewer on that property | Grant access in GA4 → Admin → Property Access Management |
| Data API returns 0 for everything, < 48h after launch | standard reports lag 24–48h on first data | Wait; use Realtime to confirm data is arriving |
| Slow dashboard / 429 quota errors | cache TTL too low or cache backend not shared across workers | Verify cache backend + TTLs (§6.3) |
| `ga_capture_token` returns no refresh token | Google only issues one on *first* consent | Revoke at myaccount.google.com/permissions, retry with `prompt="consent"` |

---

*Source implementation: the Bejundas Platform (`apps/analytics/`, `apps/core/`,
`docs/google-analytics.md`). This playbook generalizes that build for reuse on other sites.*
