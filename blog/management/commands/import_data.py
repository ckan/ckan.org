import json
import ntpath

from datetime import datetime
from html.parser import HTMLParser
from io import BytesIO

from django.core.files import File
from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from wagtail.images.models import Image

from blog.models import BlogListingPage, BlogPostPage


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            default_image = Image.objects.get(title="default.png")
        except Image.DoesNotExist:
            default_image_path = "default.png"
            with open(default_image_path, "rb") as imagefile:
                default_image = Image(
                    file=ImageFile(BytesIO(imagefile.read())),
                    title=ntpath.basename(imagefile.name),
                    width=520,
                    height=390,
                )
                default_image.file.save("default", File(imagefile))
                default_image.save()

        with open("blog_posts.json", "r") as f:
            data = json.load(f)

            for page in data:
                post_t = page.get("post_title", "")
                post_name = page.get("post_name", "")
                author = page.get("display_name", "")
                created = datetime.strptime(page.get("post_date"), "%Y-%m-%d %H:%M:%S")
                body = page.get("post_content", "")
                parser = ImgTagHTMLParser()
                parser.feed(body)
                items = parser.items
                main_image_path = ""
                if items:
                    main_image_name = ntpath.basename(items[0])
                    main_image_path = "old-site-uploads/{}/{:02d}/{}".format(
                        created.year, created.month, main_image_name
                    )
                try:
                    with open(main_image_path, "rb") as imagefile:
                        image = Image(
                            file=ImageFile(BytesIO(imagefile.read())),
                            title=ntpath.basename(imagefile.name),
                            width=520,
                            height=390,
                        )
                        image.file.save("", File(imagefile))
                        image.save()
                except FileNotFoundError:
                    image = default_image

                parent = BlogListingPage.objects.first()

                new_page = BlogPostPage(
                    main_image=image,
                    title=post_t,
                    post_title=post_t,
                    slug=post_name,
                    author=author,
                    created=created,
                    body=json.dumps(
                        [
                            {"type": "html", "value": body},
                        ]
                    ),
                    imported=True,
                )
                try:
                    parent.add_child(instance=new_page)
                    new_page.save_revision()
                    new_page.save_revision().publish()
                    self.stdout.write(f"Page created: {post_t}.")
                except ValidationError as e:
                    if "This slug is already in use" in e.messages:
                        self.stdout.write(f"Page '{post_t}' is alredy in the DB")


class ImgTagHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.items = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attrs = dict(attrs)
            if attrs.get("src", ""):
                self.items.append(attrs.get("src"))
