from rest_framework.viewsets import ModelViewSet
from api_rest.models import Usuario, Vehiculo, Viaje
from .serializer import CreateUsuarioSerializer, UsuarioSerializer, ViajeSerializer, AgregarPasajeroSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from django_filters import FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


class ViajeFilterSet(FilterSet):
    pasajero = NumberFilter(field_name='pasajeros', method='filtrar_pasajero')

    class Meta:
        model = Viaje
        fields = ['pasajero']

    def filtrar_pasajero(self, queryset, name, value):
        return queryset.exclude(**{f'{name}__id': value})


class UsuarioViewSet(ModelViewSet):
    serializer_class = CreateUsuarioSerializer
    queryset = Usuario.objects.all()
    http_method_names = ['post', 'get']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUsuarioSerializer
        
        return UsuarioSerializer

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = ViajeFilterSet


    @action(methods=['put'], detail=True)
    def agregar_pasajero(self, request, pk):
        serializer = AgregarPasajeroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        viaje = Viaje.objects.get(pk=pk)
        if serializer.validated_data['pasajero_nuevo'] in viaje.pasajeros.all().values_list('id', flat=True):
            raise ValidationError('Pasajero ya reservo este viaje')

        viaje.pasajeros.add(Usuario.objects.get(pk=serializer.validated_data['pasajero_nuevo']))

        return Response(HTTP_200_OK)
