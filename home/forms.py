from allauth.account.forms import LoginForm


class CkanorgLoginForm(LoginForm):
    """Generate ckan.org Login form

    Args:
        LoginForm (class): class inherited from 'allauth' package

    Returns:
        object: Login form object
    """

    def login(self, *args, **kwargs):
        return super(CkanorgLoginForm, self).login(*args, **kwargs)
