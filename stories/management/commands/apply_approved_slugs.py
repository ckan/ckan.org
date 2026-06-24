"""
One-time management command to apply the pre-approved SEO slugs to StoryItem records.
Slugs were manually reviewed and approved on 2026-06-24.
"""

from django.core.management.base import BaseCommand

from stories.models import StoryItem

APPROVED_SLUGS = {
    1:  "data-gov-uk-national-open-data-portal",
    3:  "hdx-humanitarian-data-exchange",
    4:  "data-gov-au-federated-open-data-australia",
    5:  "ckan-global-open-data-portals-ecosystem",
    8:  "warsaw-smart-city-open-data-portal",
    9:  "openafrica-african-open-data-repository",
    10: "civic-data-lab-india-open-data-platform",
    11: "toronto-open-data-portal-canada",
    12: "canada-government-open-data-platform-ckan",
    13: "ssen-uk-energy-smart-meter-open-data",
    14: "norwegian-refugee-council-humanitarian-data-catalog",
    15: "transport-data-commons-global-sustainable-transport",
    16: "sigma-2-norway-research-data-archive-ckan",
    17: "durban-edge-economic-intelligence-south-africa",
    18: "idb-open-data-platform-latin-america",
}


class Command(BaseCommand):
    help = "Apply pre-approved SEO slugs to StoryItem records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without saving anything.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        updated = 0
        missing = []

        for pk, slug in APPROVED_SLUGS.items():
            try:
                story = StoryItem.objects.get(pk=pk)
                old = story.slug or "(none)"
                self.stdout.write(f"  [{pk}] {story.title}")
                self.stdout.write(f"       {old} → {slug}")
                if not dry_run:
                    story.slug = slug
                    story.save(update_fields=["slug"])
                updated += 1
            except StoryItem.DoesNotExist:
                missing.append(pk)

        action = "Would update" if dry_run else "Updated"
        self.stdout.write(self.style.SUCCESS(f"\n{action} {updated} story slug(s)."))
        if missing:
            self.stdout.write(self.style.WARNING(f"Not found: IDs {missing}"))
