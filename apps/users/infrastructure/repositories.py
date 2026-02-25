from django.shortcuts import get_object_or_404
from apps.users.domain.repositories import UserRepositoryPort
from apps.users.infrastructure.models import User


class DjangoUserRepository(UserRepositoryPort):
    def create(self, data: dict):
        password = data.pop("password")
        data.pop("is_active", None)  # por si alguien lo manda igual
        return User.objects.create_user(password=password, is_active=True, **data)

    def list(self):
        return User.objects.all()

    def get_by_id(self, user_id: int):
        return get_object_or_404(User, id=user_id)

    def update(self, user, data: dict):
        password = data.pop("password", None)

        for key, value in data.items():
            setattr(user, key, value)

        if password:
            user.set_password(password)

        user.save()
        return user

    def delete(self, user):
        # borrado lógico
        user.is_active = False
        user.save(update_fields=["is_active"])
        return user

    def get_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None