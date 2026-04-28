from wagtail.models import Page
from django.conf import settings
from blog.models import BlogPostPage
from contact.models import Email, MailChimpSettings, send_contact_info
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
				member_info = {
					"email_address": email,
					"status": "subscribed",
					"merge_fields": {
						"FNAME": name.split(" ")[0] if name else "",
						"LNAME": name.split(" ")[-1] if name else "",
						"FORM": "Get Involved Form",
						"ORG": organization,
						"CKANUSE": relation,
						"MESSAGE": message,
					}
				}
				send_contact_info(request, member_info)
				context['success'] = True
			else:
				context['form_errors'] = form.errors
			context['form'] = form
		else:
			context['form'] = GetInvolvedForm()
		# Stories
		last_year_posts = BlogPostPage.objects.filter(is_story=True)
		context["stories"] = last_year_posts.order_by("story_publish_date")
		# Mailchimp
		mailchimp_settings = MailChimpSettings.for_request(request)
		context["mailchimp_api_key"] = getattr(mailchimp_settings, "api_key", "")
		context["mailchimp_audience_id"] = getattr(mailchimp_settings, "audience_id", "")
		# Recaptcha
		context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
		return context
