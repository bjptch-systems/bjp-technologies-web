"""All GA4 Data API access goes through this one module.

Every call is cached so a busy admin never exhausts the Data API's ~25k token/day
quota. The `bypass_cache` flag is what the dashboard's Refresh button uses.

The headline numbers are read from `rows[0]`, NOT `totals[0]`: with no dimensions
the API returns a single row whose metric values ARE the totals, and `totals[]`
stays empty unless `metric_aggregations` is set. Reading totals[0] is the classic
"every KPI shows 0" bug.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.core.cache import cache

# --- Conversion events (keep in sync with the ga_event names fired in templates) ---

CONVERSION_EVENT_NAMES = ("contact_submit",)
CONVERSION_EVENT_LABELS = {"contact_submit": "Contact Form"}
CONVERSION_EVENT_ICONS = {"contact_submit": "mail"}


# --- Credentials / client ---


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
    """View code checks this so a missing-env-var deploy shows a friendly setup
    page instead of a 500."""
    return bool(
        settings.GA_PROPERTY_ID
        and settings.GA_OAUTH_CLIENT_ID
        and settings.GA_OAUTH_CLIENT_SECRET
        and settings.GA_OAUTH_REFRESH_TOKEN
    )


def _property() -> str:
    return f"properties/{settings.GA_PROPERTY_ID}"


# --- Cached report runners ---


def _run_report_cached(
    cache_key,
    ttl,
    *,
    metrics,
    dimensions=(),
    start="7daysAgo",
    end="today",
    limit=None,
    bypass_cache=False,
):
    cached = None if bypass_cache else cache.get(cache_key)
    if cached is not None:
        return cached

    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )

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
            {
                "dimensions": [v.value for v in row.dimension_values],
                "metrics": [v.value for v in row.metric_values],
            }
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
        RunRealtimeReportRequest(property=_property(), metrics=[Metric(name="activeUsers")])
    )
    value = int(response.rows[0].metric_values[0].value) if response.rows else 0
    cache.set(cache_key, value, ttl)
    return value


# --- Typed helpers ---


@dataclass(frozen=True)
class Kpi:
    label: str
    value: int
    window: str


@dataclass(frozen=True)
class NamedRow:
    """A name + a single integer metric (top pages, sources, countries, devices)."""

    name: str
    value: int
    detail: str = ""


@dataclass(frozen=True)
class ConversionRow:
    event_name: str
    count: int

    @property
    def label(self) -> str:
        return CONVERSION_EVENT_LABELS.get(self.event_name, self.event_name)

    @property
    def icon(self) -> str:
        return CONVERSION_EVENT_ICONS.get(self.event_name, "bolt")


def realtime_active_users(*, bypass_cache=False) -> int:
    return _run_realtime_cached("ga:realtime:active", ttl=60, bypass_cache=bypass_cache)


def headline_kpis(*, bypass_cache=False) -> list[Kpi]:
    out: list[Kpi] = []
    for label_u, label_v, start, window in (
        ("Users (Today)", "Page Views (Today)", "today", "today"),
        ("Users (7d)", "Page Views (7d)", "7daysAgo", "last 7 days"),
        ("Users (30d)", "Page Views (30d)", "30daysAgo", "last 30 days"),
    ):
        p = _run_report_cached(
            f"ga:headline:{start}",
            ttl=1800,
            metrics=["activeUsers", "screenPageViews"],
            start=start,
            end="today",
            bypass_cache=bypass_cache,
        )
        row = (
            p["rows"][0]["metrics"]
            if p["rows"]
            else (p["totals"][0] if p["totals"] else ["0", "0"])
        )
        out.append(Kpi(label=label_u, value=int(row[0] or 0), window=window))
        out.append(Kpi(label=label_v, value=int(row[1] or 0), window=window))
    return out


def top_pages(limit=5, *, bypass_cache=False) -> list[NamedRow]:
    p = _run_report_cached(
        f"ga:top_pages:7d:{limit}",
        ttl=3600,
        metrics=["screenPageViews"],
        dimensions=["pagePath", "pageTitle"],
        start="7daysAgo",
        end="today",
        limit=limit,
        bypass_cache=bypass_cache,
    )
    rows = sorted(p["rows"], key=lambda r: int(r["metrics"][0] or 0), reverse=True)[:limit]
    return [
        NamedRow(
            name=r["dimensions"][1] or r["dimensions"][0],
            value=int(r["metrics"][0] or 0),
            detail=r["dimensions"][0],
        )
        for r in rows
    ]


def top_sources(limit=5, *, bypass_cache=False) -> list[NamedRow]:
    p = _run_report_cached(
        f"ga:top_sources:7d:{limit}",
        ttl=3600,
        metrics=["sessions"],
        dimensions=["sessionSource"],
        start="7daysAgo",
        end="today",
        limit=limit,
        bypass_cache=bypass_cache,
    )
    rows = sorted(p["rows"], key=lambda r: int(r["metrics"][0] or 0), reverse=True)[:limit]
    return [
        NamedRow(name=r["dimensions"][0] or "(direct)", value=int(r["metrics"][0] or 0))
        for r in rows
    ]


def top_countries(limit=5, *, bypass_cache=False) -> list[NamedRow]:
    p = _run_report_cached(
        f"ga:top_countries:30d:{limit}",
        ttl=3600,
        metrics=["activeUsers"],
        dimensions=["country"],
        start="30daysAgo",
        end="today",
        limit=limit,
        bypass_cache=bypass_cache,
    )
    rows = sorted(p["rows"], key=lambda r: int(r["metrics"][0] or 0), reverse=True)[:limit]
    return [
        NamedRow(name=r["dimensions"][0] or "(unknown)", value=int(r["metrics"][0] or 0))
        for r in rows
    ]


def device_breakdown(*, bypass_cache=False) -> list[NamedRow]:
    p = _run_report_cached(
        "ga:devices:30d",
        ttl=3600,
        metrics=["activeUsers"],
        dimensions=["deviceCategory"],
        start="30daysAgo",
        end="today",
        bypass_cache=bypass_cache,
    )
    rows = sorted(p["rows"], key=lambda r: int(r["metrics"][0] or 0), reverse=True)
    return [
        NamedRow(name=(r["dimensions"][0] or "unknown").title(), value=int(r["metrics"][0] or 0))
        for r in rows
    ]


def conversions_30d(*, bypass_cache=False) -> list[ConversionRow]:
    p = _run_report_cached(
        "ga:conversions:30d",
        ttl=1800,
        metrics=["eventCount"],
        dimensions=["eventName"],
        start="30daysAgo",
        end="today",
        bypass_cache=bypass_cache,
    )
    by_name = {r["dimensions"][0]: int(r["metrics"][0] or 0) for r in p["rows"]}
    # Iterate over OUR canonical list so a zero-count event still renders a card.
    return [ConversionRow(event_name=n, count=by_name.get(n, 0)) for n in CONVERSION_EVENT_NAMES]


def invalidate_all() -> None:
    cache.delete_many(
        [
            "ga:realtime:active",
            "ga:headline:today",
            "ga:headline:7daysAgo",
            "ga:headline:30daysAgo",
            "ga:top_pages:7d:5",
            "ga:top_sources:7d:5",
            "ga:top_countries:30d:5",
            "ga:devices:30d",
            "ga:conversions:30d",
        ]
    )
