from django.conf import settings

import requests


def validate_captcha(request) -> bool:
    recaptcha_response = request.POST.get("g-recaptcha-response")

    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": recaptcha_response},
    )
    result = r.json()

    return result.get("success", False)

