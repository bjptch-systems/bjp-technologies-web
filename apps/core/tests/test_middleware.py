"""Tests for the Content-Security-Policy header.

The middleware is only wired into MIDDLEWARE in production settings, so these
exercise the class directly rather than going through the test client.
"""

import pytest

from apps.core.middleware import ContentSecurityPolicyMiddleware


def build_policy():
    """Run the middleware over a stub response and parse the CSP it sets."""

    def get_response(request):
        return {}

    response = ContentSecurityPolicyMiddleware(get_response)(request=None)
    header = response["Content-Security-Policy"]

    policy = {}
    for directive in header.split(";"):
        parts = directive.split()
        if parts:
            policy[parts[0]] = set(parts[1:])
    return policy


@pytest.fixture
def policy():
    return build_policy()


def test_header_is_set():
    def get_response(request):
        return {}

    response = ContentSecurityPolicyMiddleware(get_response)(request=None)
    assert "Content-Security-Policy" in response


def test_default_src_stays_locked_to_self(policy):
    assert policy["default-src"] == {"'self'"}


def test_frame_src_allows_google_maps(policy):
    """Regression: without frame-src the Maps iframe on /contact/ was blocked.

    An absent frame-src falls back to default-src 'self', which makes the
    browser refuse the embed and render "This content is blocked".
    """
    assert "https://www.google.com" in policy["frame-src"]
    assert "https://maps.google.com" in policy["frame-src"]


def test_script_src_allows_ga4_loader(policy):
    assert "https://www.googletagmanager.com" in policy["script-src"]


def test_connect_src_allows_ga4_beacons(policy):
    assert "https://www.google-analytics.com" in policy["connect-src"]
    assert "https://*.google-analytics.com" in policy["connect-src"]
    assert "https://*.analytics.google.com" in policy["connect-src"]


def test_clickjacking_protection_retained(policy):
    """Widening frame-src must not loosen who may frame us."""
    assert policy["frame-ancestors"] == {"'none'"}


def test_no_wildcard_script_or_default_source(policy):
    for directive in ("default-src", "script-src", "connect-src", "frame-src"):
        assert "*" not in policy[directive]
        assert "https:" not in policy[directive]
