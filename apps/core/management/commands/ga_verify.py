from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Smoke-test the GA4 Data API credentials by running a small report."

    def handle(self, *args, **options):
        missing = [
            name
            for name in (
                "GA_PROPERTY_ID",
                "GA_OAUTH_CLIENT_ID",
                "GA_OAUTH_CLIENT_SECRET",
                "GA_OAUTH_REFRESH_TOKEN",
            )
            if not getattr(settings, name, "")
        ]
        if missing:
            raise CommandError(
                "Missing env vars: "
                + ", ".join(missing)
                + ". Run `ga_capture_token` first, then add them to .env."
            )

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
        resp = client.run_report(
            RunReportRequest(
                property=f"properties/{settings.GA_PROPERTY_ID}",
                date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
                metrics=[Metric(name="activeUsers"), Metric(name="screenPageViews")],
            )
        )

        row = resp.rows[0].metric_values if resp.rows else None
        users = row[0].value if row else "0"
        views = row[1].value if row else "0"
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Auth works. Last 7 days — activeUsers={users}, screenPageViews={views}."
            )
        )
        self.stdout.write("Zero values are fine if the property is < 48h old — auth is confirmed.")
