from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from api_rest.models import Usuario, Vehiculo, Viaje
from .serializer import CreateUsuarioSerializer, ViajeSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail

class UsuarioViewSet(ModelViewSet):
    serializer_class = CreateUsuarioSerializer
    queryset = Usuario.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        usuario = super().create(request, *args, **kwargs)
        if usuario.data['es_conductor']:
            vehiculo = Vehiculo.objects.create(
                conductor_id=usuario.data['id'],
                patente=request.data['patente'],
                marca=request.data['marca'],
                modelo=request.data['modelo'],
            )
            response = {
                **usuario.data,
                'patente': vehiculo.patente,
                'marca': vehiculo.marca,
                'modelo': vehiculo.modelo,
            }
            response.pop('password')

            return Response(response, HTTP_200_OK)

        return usuario

class ViajeViewSet(ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer
