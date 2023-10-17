from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import (
    BooleanField, 
    EmailField, 
    IntegerField, 
    Manager, 
    Model, 
    CharField, 
    ForeignKey, 
    FloatField, 
    DateTimeField, 
    CASCADE,
    ManyToManyField
)

class UserManager(BaseUserManager, Manager):
    """Manager for user Model"""

    use_in_migrations = True

    def _create_user(self, email, password, is_superuser, **extra_fields):
        """Base method to create user"""
        if not email:
            raise ValueError("El email es obligatorio")
        password = make_password(password)
        user = self.model(
            email=self.normalize_email(email), password=password, is_superuser=is_superuser, **extra_fields
        )
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
        return self._create_user(email, password, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = CharField(max_length=20)
    email = EmailField(verbose_name="Correo electrónico", unique=True, blank=False)
    active = BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = "email"

    groups = ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        related_name='custom_user_set'  # Set a unique related_name here
    )
    
    user_permissions = ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        related_name='custom_user_set'  # Set a unique related_name here
    )

    def save(self, args, **kwargs):
        super(User, self).save(args, **kwargs)

class Usuario(Model):
    telefono = CharField(max_length=10)
    direccion = CharField(max_length=70)

    def __str__(self):
        return str(self.nombre)

class Conductor(Model):
    usuario = ForeignKey(Usuario, on_delete=CASCADE)
    calificacion = FloatField()
    patente = CharField(max_length=6)
    modelo_vehiculo = CharField(max_length=50)

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