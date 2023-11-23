from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from api_rest.models import Usuario
from api_rest.serializer import CreateUsuarioSerializer

class UsuarioViewSet(ModelViewSet):
    serializer_class = CreateUsuarioSerializer
    queryset = Usuario.objects.all()

    http_method_names = ['post']

