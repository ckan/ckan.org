from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaBase
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractEmailForm


class ReCaptchaV2Invisible(ReCaptchaBase):
    """Customized widget for Google reCAPTCHA v2 Invisible."""

    input_type = "hidden"
    template_name = "django_recaptcha/widget_v2_invisible.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        
        # Set a unique ID for the widget to ensure it works correctly when multiple forms are present
        attrs["id"] = f"recaptcha-{self.uuid}"

        # Invisible reCAPTCHA should not have another size
        attrs["data-size"] = "invisible"
        return attrs


class WagtailCaptchaFormBuilder(FormBuilder):
	CAPTCHA_FIELD_NAME = "wagtailcaptcha"

	@property
	def formfields(self):
		fields = super(WagtailCaptchaFormBuilder, self).formfields
		fields[self.CAPTCHA_FIELD_NAME] = ReCaptchaField(widget=ReCaptchaV2Invisible(api_params={'onload': 'onloadCallback', 'explicit': 'True'}), label="")
		return fields


def remove_captcha_field(form):
	form.fields.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
	form.cleaned_data.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)


class WagtailCaptchaEmailForm(AbstractEmailForm):
	"""Pages implementing a captcha form with email notification should inherit from this."""

	form_builder = WagtailCaptchaFormBuilder

	def process_form_submission(self, form):
		remove_captcha_field(form)
		return super(WagtailCaptchaEmailForm, self).process_form_submission(form)

	class Meta: # type: ignore
		abstract = True
