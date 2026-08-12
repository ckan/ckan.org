"""
One-time management command to apply approved YouTube video URLs to StoryItem records.
URLs sourced from the CKAN Monthly Live YouTube playlist (2026-06-24).
"""

from django.core.management.base import BaseCommand

from stories.models import StoryItem

APPROVED_YOUTUBE_URLS = {
    8:  "https://youtu.be/IWDUCJLVwo0?si=3DoozKJb3eV_ciC2",  # City of Warsaw
    9:  "https://youtu.be/sFTgepAAhq4?si=ObcWOVAWDYmO8yk1",  # openAFRICA
    10: "https://youtu.be/6glMAD3dH-U?si=GtFkmtuHjMUhpXPo",  # Civic Data Lab (India)
    11: "https://youtu.be/yljTsQkJmP4?si=DcVsL-1Ypi-a_ihp",  # City of Toronto
    13: "https://youtu.be/egime4F-edg?si=c5dOLsp9_qlPk7AB",  # SSEN Distribution
    14: "https://youtu.be/6DsOAeE8rvE?si=lHpr38foKOyA5RhI",  # Norwegian Refugee Council
    15: "https://youtu.be/3Y6twYgX7zo?si=j9z2HAfkwxO8fR60",  # Transport Data Commons
    16: "https://youtu.be/pWXwtvbwSUw?si=BI84WFYCzBzLj0DW",  # Sigma 2
    17: "https://youtu.be/-TssU5xlEtI?si=c6xZuDTgM1wRfrYn",  # Durban Edge
    18: "https://youtu.be/6IJN6zckXog?si=yEeR3zV8uCjqOSUG",  # IDB
    12: "https://www.youtube.com/watch?v=9eD7HDS9PWk&t=9s",   # Government of Canada
}


class Command(BaseCommand):
    help = "Apply pre-approved YouTube URLs to StoryItem records."

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

        for pk, url in APPROVED_YOUTUBE_URLS.items():
            try:
                story = StoryItem.objects.get(pk=pk)
                old = story.youtube_url or "(none)"
                self.stdout.write(f"  [{pk}] {story.title}")
                self.stdout.write(f"       {old} → {url}")
                if not dry_run:
                    story.youtube_url = url
                    story.save(update_fields=["youtube_url"])
                updated += 1
            except StoryItem.DoesNotExist:
                missing.append(pk)

        action = "Would update" if dry_run else "Updated"
        self.stdout.write(self.style.SUCCESS(f"\n{action} {updated} story YouTube URL(s)."))
        if missing:
            self.stdout.write(self.style.WARNING(f"Not found: IDs {missing}"))
