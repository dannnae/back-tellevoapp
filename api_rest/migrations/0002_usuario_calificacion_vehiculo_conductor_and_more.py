# Generated by Django 4.1.7 on 2023-11-24 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='calificacion',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='conductor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conductor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resena',
            name='conductor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resena_conductor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resena',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resena_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='viaje',
            name='conductor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viajes_conductor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Conductor',
        ),
    ]
