from allauth.account.forms import SignupForm, LoginForm, PasswordField
from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtailcaptcha.models import WagtailCaptchaEmailForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
 
 
class CkanorgSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(
        max_length=30,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
 
    password1 = PasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Password (again)")) 
    captcha = ReCaptchaField(
        label=False,
        widget=ReCaptchaV3(
            attrs={
                'required_score':0.85,
            }
        )
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class CkanorgLoginForm(LoginForm):
    captcha = ReCaptchaField(
        label=False,
        widget=ReCaptchaV3(
            attrs={
                'required_score':0.85,
            }
        )
    )
    def login(self, *args, **kwargs):
        return super(CkanorgLoginForm, self).login(*args, **kwargs)
