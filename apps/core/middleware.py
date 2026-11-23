from django.http import HttpResponsePermanentRedirect
from django.utils.cache import patch_cache_control


class ContentSecurityPolicyMiddleware:
    """Send a Content-Security-Policy header on every response.

    Third-party origins are allowed only where the site actually needs them:

    - ``script-src``  googletagmanager.com serves the GA4 gtag.js loader.
    - ``connect-src`` GA4 sends its measurement beacons to the analytics
      endpoints; regional collectors use subdomains, hence the wildcards.
    - ``frame-src``   the contact page embeds a Google Maps iframe. Without an
      explicit ``frame-src`` the browser falls back to ``default-src 'self'``
      and refuses the frame outright.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
            "https://www.googletagmanager.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://html.themewant.com data:; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://www.google-analytics.com "
            "https://*.google-analytics.com https://*.analytics.google.com; "
            "frame-src https://www.google.com https://maps.google.com; "
            "frame-ancestors 'none';"
        )
        return response


class StripWwwMiddleware:
    """Permanently redirect www.bjptechnologies.co.tz to bjptechnologies.co.tz.

    Both hosts are allowed and served, so without this Google indexes the same pages
    twice (it already showed the contact page under www). One canonical host keeps the
    search listing and the Business Profile pointing at a single site. Runs first so
    http://www… reaches https://bjptechnologies.co.tz in one hop.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host.startswith("www."):
            return HttpResponsePermanentRedirect(f"https://{host[4:]}{request.get_full_path()}")
        return self.get_response(request)


class NoCacheHTMLMiddleware:
    """Tell the server and browsers not to keep stored copies of HTML pages.

    The host's NGINX cached whole pages, so admin changes (a cleared logo, new text) kept
    showing old versions for a while. ``private`` keeps shared caches out; ``no-cache``
    makes browsers check back each time. Static files are untouched — they keep their own
    caching. Pages that already set Cache-Control (admin, etc.) are left alone.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "Cache-Control" not in response and response.get("Content-Type", "").startswith(
            "text/html"
        ):
            patch_cache_control(response, no_cache=True, private=True)
        return response
