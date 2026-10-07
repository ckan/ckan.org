import logging

import requests
from django.conf import settings

logger = logging.getLogger("error_logger")

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_TIMEOUT_SECONDS = 5


def verify_recaptcha_token(token: str | None) -> bool:
    """Verify a reCAPTCHA response token with Google.

    Fails closed: a missing token, a network error or an unparsable response
    all return ``False`` so that form submissions are rejected rather than
    silently accepted when reCAPTCHA is unavailable.
    """
    if not token:
        return False

    try:
        response = requests.post(
            RECAPTCHA_VERIFY_URL,
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": token,
            },
            timeout=RECAPTCHA_TIMEOUT_SECONDS,
        )
        result = response.json()
    except (requests.RequestException, ValueError):
        logger.exception("reCAPTCHA verification request failed")
        return False

    return bool(result.get("success", False))


def validate_captcha(request) -> bool:
    """Validate the reCAPTCHA token submitted with a regular form POST."""
    return verify_recaptcha_token(request.POST.get("g-recaptcha-response"))

