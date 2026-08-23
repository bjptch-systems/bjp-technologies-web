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
