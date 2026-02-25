from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.auth_session.application.use_cases import AuthUseCases
from apps.auth_session.infrastructure.serializers import (
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Login exitoso (retorna usuario + tokens JWT)"),
            401: OpenApiResponse(description="Credenciales inválidas"),
        },
        summary="Iniciar sesión",
        description="Autentica usuario con email y password, y retorna access/refresh token."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_cases = AuthUseCases()
        try:
            result = use_cases.login(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
        request=PasswordResetRequestSerializer,
        responses={
            200: OpenApiResponse(description="Solicitud procesada"),
        },
        summary="Solicitar recuperación de contraseña",
        description="Envía correo con enlace de recuperación si el email existe."
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_cases = AuthUseCases()
        result = use_cases.request_password_reset(serializer.validated_data["email"])
        return Response(result, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
        request=PasswordResetConfirmSerializer,
        responses={
            200: OpenApiResponse(description="Contraseña actualizada"),
            400: OpenApiResponse(description="UID o token inválido"),
        },
        summary="Confirmar recuperación de contraseña",
        description="Recibe uid, token y nueva contraseña para actualizar la contraseña del usuario."
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_cases = AuthUseCases()
        try:
            result = use_cases.confirm_password_reset(
                uid=serializer.validated_data["uid"],
                token=serializer.validated_data["token"],
                new_password=serializer.validated_data["new_password"],
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)