"""Service-layer tests — no real API calls; the cached runner is patched."""

import pytest

from apps.analytics import services


def test_headline_kpis_reads_rows_not_totals(monkeypatch):
    """Regression for the rows[0] gotcha: with no dimensions the metric values live
    in rows[0], and totals[] is empty. Reading totals[0] would show 0 everywhere."""

    def fake_run(cache_key, ttl, **kwargs):
        return {"rows": [{"dimensions": [], "metrics": ["42", "100"]}], "totals": []}

    monkeypatch.setattr(services, "_run_report_cached", fake_run)
    kpis = services.headline_kpis()

    assert len(kpis) == 6  # users + views, across 3 windows
    assert all(k.value in (42, 100) for k in kpis)
    assert any(k.value == 42 for k in kpis)


def test_headline_kpis_falls_back_to_totals(monkeypatch):
    """If rows is empty but totals is present, use totals[0]."""

    def fake_run(cache_key, ttl, **kwargs):
        return {"rows": [], "totals": [["7", "9"]]}

    monkeypatch.setattr(services, "_run_report_cached", fake_run)
    kpis = services.headline_kpis()
    assert {k.value for k in kpis} == {7, 9}


def test_conversions_render_zero_count_cards(monkeypatch):
    """Events with no data still get a card (iterates our canonical list)."""

    def fake_run(cache_key, ttl, **kwargs):
        return {"rows": [], "totals": []}

    monkeypatch.setattr(services, "_run_report_cached", fake_run)
    rows = services.conversions_30d()
    assert [r.event_name for r in rows] == list(services.CONVERSION_EVENT_NAMES)
    assert all(r.count == 0 for r in rows)
    assert rows[0].label == "Contact Form"


@pytest.mark.parametrize(
    "env,expected",
    [
        (
            {
                "GA_PROPERTY_ID": "1",
                "GA_OAUTH_CLIENT_ID": "1",
                "GA_OAUTH_CLIENT_SECRET": "1",
                "GA_OAUTH_REFRESH_TOKEN": "1",
            },
            True,
        ),
        (
            {
                "GA_PROPERTY_ID": "",
                "GA_OAUTH_CLIENT_ID": "1",
                "GA_OAUTH_CLIENT_SECRET": "1",
                "GA_OAUTH_REFRESH_TOKEN": "1",
            },
            False,
        ),
    ],
)
def test_is_configured(settings, env, expected):
    for k, v in env.items():
        setattr(settings, k, v)
    assert services.is_configured() is expected
