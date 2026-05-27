import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


class Command(BaseCommand):
    help = "Capture a GA4 Data API refresh token via OAuth flow (one-time setup)."

    def add_arguments(self, parser):
        parser.add_argument(
            "client_secrets_file",
            type=str,
            help="Path to the OAuth client JSON downloaded from the GCP Console.",
        )

    def handle(self, *args, **options):
        from google_auth_oauthlib.flow import InstalledAppFlow

        path = Path(options["client_secrets_file"]).expanduser()
        if not path.exists():
            raise CommandError(f"Client secrets file not found: {path}")
        with open(path) as f:
            config = json.load(f)
        installed = config.get("installed") or config.get("web")
        if not installed:
            raise CommandError(
                "Not an OAuth client JSON (expected 'installed'/'web' key). "
                "Did you download a service-account key by mistake?"
            )
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
        self.stdout.write("GA_PROPERTY_ID=538536674")
        self.stdout.write("\nDO NOT commit .env.")
