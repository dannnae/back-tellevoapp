from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import (
    BooleanField, 
    EmailField, 
    IntegerField, 
    Model, 
    CharField, 
    ForeignKey, 
    FloatField, 
    DateTimeField, 
    CASCADE,
)

class GestorUsuarios(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Base method to create user"""
        if not email:
            raise ValueError("El email es obligatorio")
        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user"""
        return self._create_user(email, password, False, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        """Creates and saves new staff user"""
        return self._create_user(email, password, True, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves new superuser"""
        extra_fields.setdefault("nombre", 'asd')
        extra_fields.setdefault("telefono", 'asd')
        extra_fields.setdefault("direccion", 'asd')

        extra_fields.setdefault("active", True)
        
        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser):
    email = EmailField(verbose_name="Correo electrónico", unique=True, blank=False)
    nombre = CharField(max_length=100, default="")
    telefono = CharField(max_length=10, default="")
    direccion = CharField(max_length=70, default="")

    active = BooleanField(default=True)

    objects = GestorUsuarios()
    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.nombre)

class Conductor(Model):
    usuario = ForeignKey(Usuario, on_delete=CASCADE, related_name='datos_conductor')
    vehiculo = ForeignKey('Vehiculo', on_delete=CASCADE, related_name='conductor', null=True)
    calificacion = IntegerField()

class Vehiculo(Model):
    patente = CharField(max_length=6)
    marca =CharField(max_length=50)
    modelo = CharField(max_length=50)

class Viaje(Model):
    usuario_pasajero = ForeignKey(Usuario, on_delete=CASCADE, related_name='viajes_pasajero') 
    conductor = ForeignKey(Conductor, on_delete=CASCADE)
    fecha_hora_inicio = DateTimeField()
    fecha_hora_termino = DateTimeField()
    origen = CharField(max_length=100)
    destino = CharField(max_length=100)
    tarifa = IntegerField()

class Pago(Model):
    viaje = ForeignKey(Viaje, on_delete=CASCADE)
    monto = IntegerField()
    metodo_pago = CharField(max_length=20)
    fecha = DateTimeField()

class Resena(Model):
    usuario = ForeignKey(Usuario, on_delete=CASCADE)
    conductor = ForeignKey(Conductor, on_delete=CASCADE)
    comentario = CharField(max_length=100)
    calificacion = FloatField()