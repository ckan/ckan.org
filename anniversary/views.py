from django.conf import settings
from django.views.generic import TemplateView

from blog.models import BlogPostPage
from contact.models import Email, MailChimpSettings, send_contact_info
from .forms import GetInvolvedForm


class AnniversaryView(TemplateView):
    template_name = "anniversary/anniversary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = GetInvolvedForm()

        # Fetch all blog posts from 2026
        last_year_posts = BlogPostPage.objects.filter(created__year=2026, is_story=True)
        context["stories"] = last_year_posts.order_by("story_publish_date")
        
        # Fetch MailChimp settings for the current site/request
        request = self.request if hasattr(self, 'request') else None
        if request:
            mailchimp_settings = MailChimpSettings.for_request(request)
            context["mailchimp_api_key"] = getattr(mailchimp_settings, "api_key", "")
            context["mailchimp_audience_id"] = getattr(mailchimp_settings, "audience_id", "")
        else:
            context["mailchimp_api_key"] = ""
            context["mailchimp_audience_id"] = ""
            
        # Add recaptcha site key to context
        context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def post(self, request, *args, **kwargs):
        form = GetInvolvedForm(request.POST)
        form_name = "Get Involved Form"
        name = request.POST.get('FNAME', None)
        organization = request.POST.get('ORG', None)
        email = request.POST.get('EMAIL', None)
        relation = request.POST.get('CKANUSE', None)
        message = request.POST.get('MESSAGE', None)

        context = self.get_context_data(form=form)
        if form.is_valid():
            # Create email object and save form data in DB
            Email.objects.create(
                form_name=form_name,
                full_name=name,
                address=email,
                message=message,
            )

            member_info = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": name.split(" ")[0],
                    "LNAME": name.split(" ")[-1],
                    "FORM": form_name,
                    "ORG": organization,
                    "CKANUSE": relation,
                    "MESSAGE": message,
                }
            }
            send_contact_info(request, member_info)
            context['success'] = True
        else:
            # Add form errors to context for highlighting in template
            context['form_errors'] = form.errors
        return self.render_to_response(context)
