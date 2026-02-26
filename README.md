# Prueba Técnica Backend (Django + DRF + JWT + Swagger)

API REST construida con **Django + Django REST Framework**, autenticación **JWT**, recuperación de contraseña (vía **token + uid** con enlace único) y documentación con **Swagger (drf-spectacular)**.

> Frontend (repositorio aparte): https://github.com/Camilo2410/prueba-tecnica-front

---

## Features principales

- CRUD de usuarios (modelo custom con email como username)
- Autenticación JWT (login)
- Recuperación de contraseña:
  - Request: envía correo con link único (en desarrollo se imprime en consola)
  - Confirm: cambia la contraseña usando `uid + token`
- Swagger UI para probar endpoints
- Semilla de usuarios de prueba (script)

---

## ⚙️ Requisitos

- Python 3.10+
- pip / venv
- Docker + Docker Compose (recomendado para la base de datos)

---

## 📦 Instalación (local)

### 1) Clonar y entrar al proyecto
```bash
git clone git@github.com:Nanomagicos/front_nanomagics.git
cd Prueba_tecnica_backend
```

### 2) Crear y activar entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🔐 Variables de entorno (.env)

Crea un archivo `.env` en la raíz del proyecto (mismo nivel que `manage.py`):

Variables que usa:
```env
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

EMAIL_BACKEND=
DEFAULT_FROM_EMAIL=
FRONTEND_RESET_URL=
```

> Nota: `FRONTEND_RESET_URL` es el link que el backend incrusta en el correo de recuperación.  
> En desarrollo se imprime en la consola (console EmailBackend).

---

## 🐳 Base de datos con Docker

Se recomienda levantar MySQL con Docker para evitar problemas locales.

### 1) Levantar servicios
```bash
docker compose up -d
```

### 2) Ver logs (opcional)
```bash
docker compose logs -f
```

> Asegúrate de que `DB_HOST` y `DB_PORT` en el `.env` coincidan con tu `docker-compose.yml`.

---

## 🧱 Migraciones

### 1) Crear migraciones
```bash
python manage.py makemigrations
```

> En este proyecto el app principal de modelo es `users`.

### 2) Aplicar migraciones
```bash
python manage.py migrate
```

---

## 🌱 Seed (usuarios de prueba)

El script crea usuarios de prueba si no existen.

### Ejecutar semilla
```bash
python -m scripts.seed_users
```

Salida esperada (ejemplo):
- `Creado: sofia.martinez@test.com`
- `Ya existe: ...`

---

## ▶️ Ejecutar servidor

```bash
python manage.py runserver
```

API disponible en:
- http://127.0.0.1:8000/

---

## 📚 Swagger (documentación / pruebas)

Swagger UI:
- http://127.0.0.1:8000/api/docs/

Schema:
- http://127.0.0.1:8000/api/schema/

---

## 🔑 Flujo de prueba (Swagger)

### 1) Login (JWT)
Endpoint:
- `POST /api/auth/login/`

Body ejemplo:
```json
{
  "email": "sofia.martinez@test.com",
  "password": "User12345"
}
```

Respuesta (ejemplo):
- tokens JWT (access/refresh) + info de usuario

### 2) Probar endpoints protegidos (Users)
Todos los endpoints de `/api/users/**` requieren JWT.

En Swagger:
1. Copia el `access token`
2. Click en **Authorize**
3. Pega:
   ```
   Bearer <ACCESS_TOKEN>
   ```

Endpoints:
- `GET /api/users/` (listar)
- `POST /api/users/` (crear)
- `GET /api/users/{id}/` (detalle)
- `PUT/PATCH /api/users/{id}/` (editar)
- `DELETE /api/users/{id}/` (desactivar / borrado lógico)

---

## 🔁 Recuperación de contraseña (flujo completo)

### 1) Solicitar reset
Endpoint:
- `POST /api/auth/password-reset/request/`

Body:
```json
{
  "email": "sofia.martinez@test.com"
}
```

Como `EMAIL_BACKEND` está en consola, verás en la terminal del backend un correo simulado con un link, por ejemplo:
```
http://localhost:5173/reset-password?uid=...&token=...
```

### 2) Confirmar reset (cambiar contraseña)
Endpoint:
- `POST /api/auth/password-reset/confirm/`

Body:
```json
{
  "uid": "<UID_DEL_LINK>",
  "token": "<TOKEN_DEL_LINK>",
  "new_password": "NuevaClave123"
}
```

Luego prueba login con la nueva contraseña.

---

## 🔒 Nota importante sobre permisos (según la prueba)

La prueba técnica solicitó:
- Autenticación JWT
- CRUD protegido (que requiera estar autenticado)

Por ello, la API implementa que **cualquier usuario autenticado** puede:
- listar usuarios
- crear usuarios
- editar usuarios
- desactivar usuarios

No se implementaron roles (admin/user) ni reglas del tipo “solo puedes editarte a ti mismo”, porque **no fue un requerimiento** del enunciado.  
Si se necesitara, se puede agregar fácilmente con permisos custom o validando `request.user` vs `user_id`.

---

## 🧪 Endpoints principales

### Auth
- `POST /api/auth/login/`
- `POST /api/auth/password-reset/request/`
- `POST /api/auth/password-reset/confirm/`

### Users (JWT requerido)
- `GET /api/users/`
- `POST /api/users/`
- `GET /api/users/{user_id}/`
- `PUT /api/users/{user_id}/`
- `PATCH /api/users/{user_id}/`
- `DELETE /api/users/{user_id}/` (borrado lógico → `is_active = false`)

---

## 🛠️ Troubleshooting rápido

### Puerto ocupado (runserver)
```bash
python manage.py runserver 8001
```

### Si no conecta a MySQL
- Verifica `DB_HOST`, `DB_PORT` en `.env`
- Verifica contenedor:
```bash
docker ps
docker compose logs -f
```

---

## 📄 Licencia
Uso libre para fines de evaluación/prueba técnica.