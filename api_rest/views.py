from rest_framework.viewsets import ModelViewSet
from api_rest.models import Usuario, Vehiculo, Viaje
from .serializer import CreateUsuarioSerializer, ViajeSerializer, AgregarPasajeroSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.decorators import action


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

    @action(methods=['put'], detail=True)
    def agregar_pasajero(self, request, pk):
        serializer = AgregarPasajeroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        viaje = Viaje.objects.get(pk=pk)
        viaje.pasajeros.add(Usuario.objects.get(pk=serializer.validated_data['pasajero_nuevo']))

        return Response(HTTP_200_OK)
    