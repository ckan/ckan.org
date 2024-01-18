from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractEmailForm

from captcha.fields import CaptchaField


class WagtailCaptchaFormBuilder(FormBuilder):
    CAPTCHA_FIELD_NAME = 'wagtailcaptcha'

    @property
    def formfields(self):
        fields = super(WagtailCaptchaFormBuilder, self).formfields
        fields[self.CAPTCHA_FIELD_NAME] = CaptchaField(label='')

        return fields


def remove_captcha_field(form):
    form.fields.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
    form.cleaned_data.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)


class WagtailCaptchaEmailForm(AbstractEmailForm):
    """
    Pages implementing a captcha form with email notification should inherit from this
    """

    form_builder = WagtailCaptchaFormBuilder

    def process_form_submission(self, form):
        remove_captcha_field(form)
        return super(WagtailCaptchaEmailForm, self).process_form_submission(form)

    class Meta:
        abstract = True
