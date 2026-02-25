import os
import sys
from pathlib import Path

# Agregar la raíz del proyecto al PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import django  # noqa: E402

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.users.infrastructure.models import User  # noqa: E402


def run():
    users = [
        # Admin / Superuser
        {
            "full_name": "Admin Prueba",
            "email": "admin@test.com",
            "password": "Admin123*",
            "is_staff": True,
            "is_superuser": True,
        },

        {"full_name": "Sofía Martínez", "email": "sofia.martinez@test.com", "password": "User12345"},
        {"full_name": "Mateo García", "email": "mateo.garcia@test.com", "password": "User12345"},
        {"full_name": "Valentina Rodríguez", "email": "valentina.rodriguez@test.com", "password": "User12345"},
        {"full_name": "Santiago López", "email": "santiago.lopez@test.com", "password": "User12345"},
        {"full_name": "Isabella Hernández", "email": "isabella.hernandez@test.com", "password": "User12345"},
        {"full_name": "Juan Pablo Pérez", "email": "juanpablo.perez@test.com", "password": "User12345"},
        {"full_name": "Camila González", "email": "camila.gonzalez@test.com", "password": "User12345"},
        {"full_name": "Daniela Torres", "email": "daniela.torres@test.com", "password": "User12345"},
        {"full_name": "Alejandro Ramírez", "email": "alejandro.ramirez@test.com", "password": "User12345"},
        {"full_name": "Mariana Flores", "email": "mariana.flores@test.com", "password": "User12345"},
        {"full_name": "Sebastián Vargas", "email": "sebastian.vargas@test.com", "password": "User12345"},
    ]

    for data in users:
        payload = data.copy()  # para no mutar la lista original
        email = payload["email"]

        if User.objects.filter(email=email).exists():
            print(f"Ya existe: {email}")
            continue

        password = payload.pop("password")

        if payload.get("is_superuser"):
            User.objects.create_superuser(password=password, **payload)
        else:
            User.objects.create_user(password=password, **payload)

        print(f"Creado: {email}")

    print("Semilla finalizada")


if __name__ == "__main__":
    run()