from contact.models import MailChimpSettings
from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Site

from stories.mailchimp import sync_story_subscriber
from stories.models import StoriesNotificationEmail


class Command(BaseCommand):
    help = (
        'Sync every "Get notified of new stories" sign-up to the Mailchimp stories '
        "audience. Safe to re-run: existing members are left as they are, new ones "
        "get Mailchimp's opt-in confirmation e-mail."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only report how many sign-ups would be synced.",
        )

    def handle(self, *args, dry_run=False, **options):
        site = Site.objects.filter(is_default_site=True).first()
        if site is None:
            raise CommandError("No default Wagtail site is configured.")
        mailchimp_settings = MailChimpSettings.for_site(site)
        if not (mailchimp_settings.api_key and mailchimp_settings.stories_audience_id):
            raise CommandError(
                "Set the Mailchimp API key and the success stories audience ID in "
                "Settings > MailChimp settings first."
            )

        emails = StoriesNotificationEmail.objects.order_by("created").values_list("email", flat=True)
        total = emails.count()
        if dry_run:
            self.stdout.write(f"{total} sign-up(s) would be synced to the stories audience.")
            return

        failed = sum(1 for email in emails.iterator() if not sync_story_subscriber(mailchimp_settings, email))
        self.stdout.write(self.style.SUCCESS(f"Synced {total - failed} of {total} sign-up(s)."))
        if failed:
            self.stdout.write(self.style.WARNING(
                f"{failed} failed - see the error log, then re-run this command."
            ))
