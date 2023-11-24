from rest_framework.serializers import ModelSerializer, CharField
from api_rest.models import Usuario
from django.contrib.auth.hashers import make_password

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
