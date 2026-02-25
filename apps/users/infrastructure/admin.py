from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.infrastructure.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ("-created_at",)
    list_display = ("id", "full_name", "email", "is_active", "is_staff", "created_at")
    list_filter = ("is_active", "is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("full_name",)}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login", "created_at")}),
    )
    readonly_fields = ("created_at", "last_login")

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_active", "is_staff"),
        }),
    )

    search_fields = ("email", "full_name")