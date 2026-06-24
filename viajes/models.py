import os
from django.db import models
from django.contrib.auth.models import User


class Viaje(models.Model):
    id = models.AutoField(primary_key=True)
    foto = models.FileField(upload_to='viajes/', null=True, blank=True)
    destino = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('concluido', 'Concluido'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    DEPARTAMENTO_CHOICES = [
        ('ventas', 'Ventas'),
        ('soporte', 'Soporte'),
        ('direccion', 'Dirección'),
    ]
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTO_CHOICES)

    requiere_anticipo = models.BooleanField(default=False)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.destino} - {self.estado}"


class Recibo(models.Model):
    id = models.AutoField(primary_key=True)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='recibos')
    pdf = models.FileField(upload_to='recibos/', null=True, blank=True)
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    TIPO_GASTO_CHOICES = [
        ('hospedaje', 'Hospedaje'),
        ('alimentacion', 'Alimentación'),
        ('transporte', 'Transporte'),
    ]
    tipo_gasto = models.CharField(max_length=20, choices=TIPO_GASTO_CHOICES)

    fecha_emision = models.DateField()

    def __str__(self):
        return f"{self.concepto} - ${self.monto}"
