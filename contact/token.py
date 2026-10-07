from typing import Any

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    """Token generator keyed on an arbitrary identifier instead of a User.

    Django's ``PasswordResetTokenGenerator`` is typed for ``AbstractBaseUser``
    instances, but this project passes the subscriber's email address (a
    ``str``) to ``make_token`` and an ``Email`` instance (whose ``__str__`` is
    the address) to ``check_token``. Typing the ``user`` argument as ``Any``
    reflects that real usage without changing behaviour.
    """

    def _make_hash_value(self, user: Any, timestamp: Any) -> str:
        return (
            text_type(user) + text_type(timestamp)
        )

    def make_token(self, user: Any) -> str:
        return super().make_token(user)

    def check_token(self, user: Any, token: str | None) -> bool:
        return super().check_token(user, token)


user_activation_token = TokenGenerator()