from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


class PasswordResetTokenService:
    token_generator = PasswordResetTokenGenerator()

    @classmethod
    def make_reset_payload(cls, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = cls.token_generator.make_token(user)
        return uid, token

    @classmethod
    def validate_token(cls, user, token: str) -> bool:
        return cls.token_generator.check_token(user, token)

    @staticmethod
    def decode_uid(uid: str):
        return force_str(urlsafe_base64_decode(uid))