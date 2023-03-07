from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type  


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, timestamp):
        return (
            text_type(email) + text_type(timestamp)
        )
user_activation_token = TokenGenerator()