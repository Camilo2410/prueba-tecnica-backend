# apps/auth_session/api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth_session.api.views import (
    LoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),

    # refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path("password-reset/request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]