from functools import wraps

from django.conf import settings

import requests


def check_recaptcha(required_score):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, required_score=required_score, *args, **kwargs):
            request.recaptcha_is_valid = None
            if request.method == "POST":
                recaptcha_response = request.POST.get("g-recaptcha-response")
                data = {
                    "secret": settings.RECAPTCHA_PRIVATE_KEY,
                    "response": recaptcha_response,
                }
                r = requests.post(
                    "https://www.google.com/recaptcha/api/siteverify", data=data
                )
                result = r.json()

                score = float(result.get("score", 0))
                required_score = float(required_score)

                if result["success"] and required_score < score:
                    request.recaptcha_is_valid = True
                else:
                    request.recaptcha_is_valid = False
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
