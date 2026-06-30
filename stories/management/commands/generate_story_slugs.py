"""
Management command to bulk-generate SEO-friendly slugs for StoryItem records.

SEO slug rules applied:
  - Based on story title only (not org prefix)
  - Lowercase, hyphens instead of spaces
  - Stop words removed when the slug remains meaningful
  - Max 6 words to keep URLs short
  - Guaranteed unique within the StoryItem table
  - Existing slugs are never overwritten unless --force is passed
"""

import re

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from stories.models import StoryItem

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "was", "are", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "shall",
    "how", "our", "their", "its", "we", "they", "it", "this", "that",
    "as", "into", "about", "up", "out", "than", "so",
}

MAX_WORDS = 6


def seo_slug(title):
    """Return a short, keyword-rich slug from a story title."""
    # Strip possessives before slugifying so "India's" → "india" not "indias"
    clean = re.sub(r"['’]s\b", "", title)
    words = slugify(clean).split("-")
    # Remove stop words, but only if at least 2 meaningful words remain
    filtered = [w for w in words if w and w not in STOP_WORDS]
    if len(filtered) < 2:
        filtered = [w for w in words if w]  # fall back to all words
    slug = "-".join(filtered[:MAX_WORDS])
    return slug or "story"


def unique_slug(base, exclude_pk):
    """Ensure slug is unique, appending a counter if needed."""
    slug = base
    counter = 2
    while StoryItem.objects.filter(slug=slug).exclude(pk=exclude_pk).exists():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


class Command(BaseCommand):
    help = "Generate SEO-friendly slugs for StoryItem records that have no slug."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate slugs even for stories that already have one.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without saving anything.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        dry_run = options["dry_run"]

        stories = StoryItem.objects.all().order_by("id")
        if not force:
            stories = stories.filter(slug="")

        if not stories.exists():
            self.stdout.write(self.style.SUCCESS("All stories already have slugs. Use --force to regenerate."))
            return

        updated = 0
        for story in stories:
            base = seo_slug(story.title)
            new_slug = unique_slug(base, exclude_pk=story.pk)
            old_slug = story.slug or "(none)"

            self.stdout.write(f"  [{story.pk}] {story.title}")
            self.stdout.write(f"       {old_slug} → {new_slug}")

            if not dry_run:
                story.slug = new_slug
                story.save(update_fields=["slug"])
            updated += 1

        action = "Would update" if dry_run else "Updated"
        self.stdout.write(self.style.SUCCESS(f"\n{action} {updated} story slug(s)."))
