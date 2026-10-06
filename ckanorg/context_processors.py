from django.conf import settings


def recaptcha(request):
    """Expose the reCAPTCHA public site key to every template.

    The newsletter signup form lives in the global footer, so the key has to be
    present on *every* page - not only on the pages that happen to add it to
    their own context manually. Without it the invisible reCAPTCHA never
    renders and the protected endpoints would reject legitimate submissions.
    """
    return {"recaptcha_sitekey": getattr(settings, "RECAPTCHA_PUBLIC_KEY", "")}
