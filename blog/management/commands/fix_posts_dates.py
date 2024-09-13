from datetime import datetime
from prettytable import PrettyTable
from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError

from blog.models import BlogPostPage


class Command(BaseCommand): 
	help = "Set first_publushed_at date as create date for old posts"

	def handle(self, *args, **kwargs):
		table = PrettyTable()
		target_date = datetime(2021, 4, 21)
		try:
			posts = BlogPostPage.objects.filter(created__lt=target_date).order_by(
					"created"
				)
		except Exception as e:
			raise CommandError(f"ERROR: {e}")

		self.stdout.write(self.style.WARNING(
			f"Total number of posts to be changed (with first published date less than April 21, 2021): {len(posts)}"
		))

		table.align = "l"
		table.field_names = ["first_published_at", "created", "post_title"]
		for post in posts:
			table.add_row([
				post.first_published_at, post.created, post.post_title
			])
		print(table)

		try:
			for post in tqdm(posts):
				post.first_published_at = post.created
				post.save()
		except Exception as e:
			raise CommandError(f"ERROR: {e}")

		self.stdout.write(self.style.SUCCESS("Completed successfully"))
