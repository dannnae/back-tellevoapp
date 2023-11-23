from rest_framework.routers import SimpleRouter
from .views import (
    UsuarioViewSet
)

router = SimpleRouter()

router.register(r'usuarios', UsuarioViewSet, basename='Usuario')
