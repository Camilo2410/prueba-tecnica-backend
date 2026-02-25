from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from apps.users.infrastructure.models import User
from apps.auth_session.infrastructure.jwt_service import JWTService
from apps.auth_session.infrastructure.token_service import PasswordResetTokenService
from apps.auth_session.infrastructure.email_service import EmailService


class AuthUseCases:
    def login(self, email: str, password: str):
        user = authenticate(username=email, password=password)

        if not user:
            raise ValueError("Credenciales inválidas.")

        if not user.is_active:
            raise ValueError("El usuario está inactivo.")

        tokens = JWTService.generate_tokens_for_user(user)
        return {
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "is_active": user.is_active,
            },
            "tokens": tokens,
        }

    def request_password_reset(self, email: str):
        user = User.objects.filter(email=email).first()
        # no revelar si existe o no el correo
        if not user:
            return {"message": "Si el correo existe, se enviará un enlace de recuperación."}

        uid, token = PasswordResetTokenService.make_reset_payload(user)
        reset_link = f"{settings.FRONTEND_RESET_URL}?uid={uid}&token={token}"

        EmailService.send_password_reset_email(user.email, reset_link)

        return {"message": "Si el correo existe, se enviará un enlace de recuperación."}

    def confirm_password_reset(self, uid: str, token: str, new_password: str):
        try:
            user_id = PasswordResetTokenService.decode_uid(uid)
            user = get_object_or_404(User, pk=user_id)
        except Exception:
            raise ValueError("UID inválido.")

        if not PasswordResetTokenService.validate_token(user, token):
            raise ValueError("Token inválido o expirado.")

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return {"message": "Contraseña actualizada correctamente."}