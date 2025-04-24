from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class HorarioAtencion(models.Model):
    hora_inicio = models.TimeField(default='07:00')
    hora_fin = models.TimeField(default='19:00')

    class Meta:
        verbose_name = "Horario de atención"
        verbose_name_plural = "Horario de atención"

    def __str__(self):
        return f"Horario: {self.hora_inicio} - {self.hora_fin}"
class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    intervalo_minutos = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(10), MaxValueValidator(180)],
        help_text="Duración en minutos del tratamiento. Esto determina cuánto bloquea en el horario."
    )
    precio = models.CharField(max_length=20)  # Ejemplo: '₡25,000'
    imagen = models.ImageField(upload_to='tratamientos/', blank=True, null=True)

    def __str__(self):
        return self.nombre



class Cita(models.Model):
    calendar_event_id = models.CharField(max_length=200, blank=True, null=True)
    nombre_cliente = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    tratamiento = models.ForeignKey('Tratamiento', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    comentarios = models.TextField(blank=True, null=True)
    creada = models.DateTimeField(auto_now_add=True)
    especialista = models.ForeignKey('Especialista', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.nombre_cliente} - {self.tratamiento.nombre} - {self.fecha} {self.hora}"

    def fin_estimado(self):
        from datetime import datetime, timedelta
        inicio_dt = datetime.combine(self.fecha, self.hora)
        fin_dt = inicio_dt + timedelta(minutes=self.tratamiento.intervalo_minutos)
        return fin_dt.time()

class BloqueoHorario(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Bloqueo de horario"
        verbose_name_plural = "Bloqueos de horario"

    def __str__(self):
        return f"Bloqueado: {self.fecha} de {self.hora_inicio} a {self.hora_fin}"

class Especialista(models.Model):
    nombre = models.CharField(max_length=100)
    especialidades = models.ManyToManyField('Tratamiento', related_name='especialistas', blank=True)

    def __str__(self):
        return self.nombre
