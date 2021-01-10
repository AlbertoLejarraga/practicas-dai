# mi_aplicacion/models.py
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta, datetime
class Autor(models.Model):
    nombre      = models.CharField(max_length=200)
    apellidos   = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre + " " + self.apellidos

class Libro(models.Model):
    isbn    = models.CharField(max_length=13, validators=[RegexValidator(regex='^.{13}$')])
    titulo  = models.CharField(max_length=200)
    autor   = models.ManyToManyField(Autor)
    imagen  = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo

class Usuario(models.Model):
    class Tipo(models.TextChoices):
        STAFF = "s", _("Personal de administración")
        CLIENTE = "c", _("Cliente de la biblioteca")

    dni         = models.CharField(max_length=9)
    nombre      = models.CharField(max_length=200)
    apellidos   = models.CharField(max_length=200)
    tipo        = models.CharField(max_length=1, choices=Tipo.choices, default=Tipo.CLIENTE)

    def __str__(self):
        return self.nombre + " " + self.apellidos

class Prestamo(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "a", _("Activo")
        FINALIZADO = "f", _("Finalizado")

    fecha           = models.DateField(default=timezone.now)
    duracion_dias   = models.IntegerField(default=30)
    libro           = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario         = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado          = models.CharField(max_length=2, choices=Estado.choices, default=Estado.ACTIVO)
    def fechaDevolucion(self):
        fechaDev = self.fecha  + timedelta(self.duracion_dias)
        return fechaDev
    def caducado(self):
        return self.fechaDevolucion() <= date.today()
