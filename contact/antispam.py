"""Minimal honeypot protection for the public forms.

reCAPTCHA is not a reliable bot filter on its own: an automated browser can
obtain a valid token without ever solving a challenge (verified against the
live site), and the old code trusted that token alone. Every public form
therefore also renders a hidden ``website`` field. A human never sees or fills
it in, a browser submits it empty, and a bot script either fills it in or
omits it entirely - in both bot cases the submission is dropped.
"""

HONEYPOT_FIELD = "website"


def honeypot_triggered(data) -> bool:
    """Return ``True`` when a submission did not come from our own form.

    ``data`` is the submitted POST data (a ``QueryDict`` or a plain mapping).
    """
    if HONEYPOT_FIELD not in data:
        return True
    return bool((data.get(HONEYPOT_FIELD) or "").strip())
