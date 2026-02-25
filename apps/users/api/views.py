from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from apps.users.application.use_cases import UserUseCases
from apps.users.infrastructure.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserResponseSerializer,
)
from apps.users.api.permissions import IsAuthenticatedUserEndpoints


class UserListCreateView(APIView):
    permission_classes = [IsAuthenticatedUserEndpoints]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_cases = UserUseCases()

    @extend_schema(
        tags=["users"],
        responses={200: UserResponseSerializer(many=True)},
        summary="Listar usuarios",
        description="Retorna la lista de usuarios. Requiere JWT."
    )
    def get(self, request):
        users = self.use_cases.list_users()
        serializer = UserResponseSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["users"],
        request=UserCreateSerializer,
        responses={
            201: UserResponseSerializer,
            400: OpenApiResponse(description="Errores de validación"),
        },
        summary="Crear usuario",
        description="Crea un usuario nuevo. Requiere JWT."
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.use_cases.create_user(serializer.validated_data)
        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticatedUserEndpoints]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_cases = UserUseCases()

    @extend_schema(
        tags=["users"],
        parameters=[
            OpenApiParameter(name="user_id", type=int, location=OpenApiParameter.PATH, required=True)
        ],
        responses={200: UserResponseSerializer},
        summary="Obtener usuario por ID",
        description="Retorna el detalle de un usuario por ID. Requiere JWT."
    )
    def get(self, request, user_id: int):
        user = self.use_cases.retrieve_user(user_id)
        serializer = UserResponseSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        tags=["users"],
        parameters=[
            OpenApiParameter(name="user_id", type=int, location=OpenApiParameter.PATH, required=True)
        ],
        request=UserUpdateSerializer,
        responses={200: UserResponseSerializer},
        summary="Actualizar usuario (PUT)",
        description="Actualiza completamente un usuario. Requiere JWT."
    )
    def put(self, request, user_id: int):
        user = self.use_cases.retrieve_user(user_id)
        serializer = UserUpdateSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = self.use_cases.update_user(user_id, serializer.validated_data)
        return Response(UserResponseSerializer(updated_user).data)

    @extend_schema(
        tags=["users"],
        parameters=[
            OpenApiParameter(name="user_id", type=int, location=OpenApiParameter.PATH, required=True)
        ],
        request=UserUpdateSerializer,
        responses={200: UserResponseSerializer},
        summary="Actualizar usuario parcialmente (PATCH)",
        description="Actualiza parcialmente un usuario. Requiere JWT."
    )
    def patch(self, request, user_id: int):
        user = self.use_cases.retrieve_user(user_id)
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_user = self.use_cases.update_user(user_id, serializer.validated_data)
        return Response(UserResponseSerializer(updated_user).data)

    @extend_schema(
        tags=["users"],
        parameters=[
            OpenApiParameter(name="user_id", type=int, location=OpenApiParameter.PATH, required=True)
        ],
        responses={
            200: OpenApiResponse(description="Usuario desactivado correctamente")
        },
        summary="Desactivar usuario",
        description="Realiza borrado lógico (is_active=False). Requiere JWT."
    )
    def delete(self, request, user_id: int):
        self.use_cases.deactivate_user(user_id)
        return Response(
            {"message": "Usuario desactivado correctamente."},
            status=status.HTTP_200_OK
        )