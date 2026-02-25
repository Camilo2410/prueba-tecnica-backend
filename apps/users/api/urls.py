from django.urls import path
from apps.users.api.views import UserListCreateView, UserDetailView

urlpatterns = [
    path("", UserListCreateView.as_view(), name="users-list-create"),
    path("<int:user_id>/", UserDetailView.as_view(), name="users-detail"),
]