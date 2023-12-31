from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
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
    ManyToManyField
)
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail
from django.conf import settings

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
    es_conductor = BooleanField(default=False)
    calificacion = FloatField(default=0.0)

    active = BooleanField(default=True)

    objects = GestorUsuarios()
    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.nombre)
    

class Vehiculo(Model):
    conductor = ForeignKey(Usuario, on_delete=CASCADE, related_name='conductor', null=True)
    patente = CharField(max_length=6)
    marca = CharField(max_length=50)
    modelo = CharField(max_length=50)


class Viaje(Model):
    pasajeros = ManyToManyField(Usuario, related_name='viajes_pasajero')
    conductor = ForeignKey(Usuario, on_delete=CASCADE, related_name='viajes_conductor')
    fecha_hora_inicio = DateTimeField()
    origen = CharField(max_length=100)
    latitud = FloatField(null=True)
    longitud = FloatField(null=True)
    tarifa = IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(3000)])


class Pago(Model):
    viaje = ForeignKey(Viaje, on_delete=CASCADE)
    monto = IntegerField()
    metodo_pago = CharField(max_length=20)
    fecha = DateTimeField()

class Resena(Model):
    usuario = ForeignKey(Usuario, on_delete=CASCADE, related_name='resena_usuario')
    conductor = ForeignKey(Usuario, on_delete=CASCADE, related_name='resena_conductor')
    comentario = CharField(max_length=100)
    calificacion = FloatField()


@receiver(m2m_changed, sender=Viaje.pasajeros.through, dispatch_uid="mandar_correo")
def mandar_correo(sender, instance: Viaje, pk_set: set, action, **kwargs):
    if action == 'post_add':
        usuario = Usuario.objects.get(pk=pk_set.pop())
        
        conductor = instance.conductor
        conductor_nombre = conductor.nombre
        hora_viaje = instance.fecha_hora_inicio
        origen_viaje = instance.origen
        tarifa_viaje = instance.tarifa
        
        send_mail(
            'Reserva exitosa', 
            f'La reserva se ha hecho correctamente para el viaje que inicia a las {hora_viaje}. '
            f'El origen del viaje es {origen_viaje} y la tarifa es {tarifa_viaje}.',
            settings.EMAIL_HOST_USER,
            [usuario.email]
        )
        send_mail(
            'Pasajero nuevo', 
            f'Un pasajero ha realizado reserva en tu viaje. '
            f'El origen del viaje es {origen_viaje} y la tarifa es {tarifa_viaje}.',
            settings.EMAIL_HOST_USER,
            [conductor.email]
        )
