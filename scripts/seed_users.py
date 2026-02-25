import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.users.infrastructure.models import User  # noqa


def run():
    users = [
        {
            "full_name": "Admin Prueba",
            "email": "admin@test.com",
            "password": "Admin123*",
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
        },
        {
            "full_name": "Usuario Activo",
            "email": "user1@test.com",
            "password": "User12345",
            "is_active": True,
        },
        {
            "full_name": "Usuario Inactivo",
            "email": "user2@test.com",
            "password": "User12345",
            "is_active": False,
        },
    ]

    for data in users:
        email = data["email"]
        if User.objects.filter(email=email).exists():
            print(f"Ya existe: {email}")
            continue

        password = data.pop("password")
        if data.get("is_superuser"):
            User.objects.create_superuser(password=password, **data)
        else:
            User.objects.create_user(password=password, **data)

        print(f"Creado: {email}")

    print("Semilla finalizada ✅")


if __name__ == "__main__":
    run()