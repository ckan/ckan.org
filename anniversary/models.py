from django.conf import settings
from django.core.mail import send_mail

from wagtail.models import Page

from blog.models import BlogPostPage
from contact.models import Email
from .forms import GetInvolvedForm

class AnniversaryPage(Page):
	parent_page_types = ["home.HomePage"]
	template = "anniversary/anniversary.html"
	max_count = 1  # Only one anniversary page

	content_panels = Page.content_panels + [
	]

	class Meta: # type: ignore
		verbose_name = "Anniversary Page"
		verbose_name_plural = "Anniversary Pages"

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		# Add the form
		if request.method == "POST":
			form = GetInvolvedForm(request.POST)
			if form.is_valid():
				name = request.POST.get('FNAME', None)
				organization = request.POST.get('ORG', None)
				email = request.POST.get('EMAIL', None)
				relation = request.POST.get('CKANUSE', None)
				message = request.POST.get('MESSAGE', None)
				Email.objects.create(
					form_name="Get Involved Form",
					full_name=name,
					address=email,
					message=message,
				)
				body = (
					f"Name: {name}\n"
					f"Email: {email}\n"
					f"Organization: {organization}\n"
					f"Relationship to CKAN: {relation}\n\n"
					f"Message:\n{message}"
				)
				send_mail(
					subject=f"[CKAN 20th] New 'Get Involved' submission from {name}",
					message=body,
					from_email=settings.DEFAULT_FROM_EMAIL,
					recipient_list=["comms@ckan.org"],
					fail_silently=True,
				)
				context['success'] = True
			else:
				context['form_errors'] = form.errors
			context['form'] = form
		else:
			context['form'] = GetInvolvedForm()
		# Stories
		last_year_posts = BlogPostPage.objects.filter(is_story=True)
		context["stories"] = last_year_posts.order_by("story_publish_date")
		# Recaptcha
		context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
		return context
