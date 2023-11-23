from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.validators import ValidationError
from api_rest.models import Usuario

class CreateUsuarioSerializer(ModelSerializer):    
    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'password')

    