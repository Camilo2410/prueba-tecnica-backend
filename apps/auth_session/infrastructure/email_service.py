from django.conf import settings
from django.core.mail import send_mail


class EmailService:
    @staticmethod
    def send_password_reset_email(to_email: str, reset_link: str):
        subject = "Recuperación de contraseña"
        message = (
            "Hola,\n\n"
            "Recibimos una solicitud para recuperar tu contraseña.\n"
            f"Usa este enlace para restablecerla:\n{reset_link}\n\n"
            "Si no solicitaste este cambio, puedes ignorar este correo."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )