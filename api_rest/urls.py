from rest_framework.routers import SimpleRouter
from .views import (
    UsuarioViewSet,
    ViajeViewSet
    
)

router = SimpleRouter()

router.register(r'usuarios', UsuarioViewSet, basename='Usuario')
router.register(r'viajes', ViajeViewSet, basename='Viaje')

