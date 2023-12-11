from rest_framework.serializers import ModelSerializer, CharField, Serializer, IntegerField, SerializerMethodField
from api_rest.models import Usuario, Viaje
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

class CreateUsuarioSerializer(ModelSerializer):
    patente = CharField(required=False, read_only=True)
    marca = CharField(required=False, read_only=True)
    modelo = CharField(required=False, read_only=True)

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'nombre', 'password', 'es_conductor', 'patente', 'marca', 'modelo')

    def create(self, validated_data):
        user = Usuario.objects.create(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            password=make_password(validated_data['password']),
            es_conductor=validated_data['es_conductor']
        )
        
        return user

class ViajeSerializer(ModelSerializer):
    nombre_conductor = CharField(required=False, read_only=True, source='conductor.nombre')
    hora_formateada = SerializerMethodField()

    
    class Meta:
        model = Viaje
        fields = ('id', 'conductor', 'hora_formateada', 'origen', 'tarifa', 'nombre_conductor', 'latitud', 'longitud', 'fecha_hora_inicio')

    def get_hora_formateada(self, viaje: Viaje):
        return viaje.fecha_hora_inicio.strftime('%d-%m-%Y %H:%M')


class AgregarPasajeroSerializer(Serializer):
    pasajero_nuevo = IntegerField(min_value=1)

    def validate_pasajero_nuevo(self, pasajero_nuevo):
        user_query = Usuario.objects.filter(pk=pasajero_nuevo)

        if not user_query:
            raise ValidationError(f'Pasajero con id {pasajero_nuevo} no existe')
        
        user = user_query.first()
        
        if user.es_conductor:
            raise ValidationError(f'Pasajero con id {pasajero_nuevo} debe ser un pasajero')
        
        return pasajero_nuevo
    
class UsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre', 'email', 'telefono', 'es_conductor')
