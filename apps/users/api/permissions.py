from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedUserEndpoints(IsAuthenticated):
    """
    Alias para autenticar endpoindts de usuario.
    """
    pass