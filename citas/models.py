from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo que define el horario general de atención
class HorarioAtencion(models.Model):
    hora_inicio = models.TimeField(default='07:00')  # Hora en que inicia la atención
    hora_fin = models.TimeField(default='19:00')     # Hora en que finaliza la atención

    class Meta:
        verbose_name = "Horario de atención"
        verbose_name_plural = "Horario de atención"

    def __str__(self):
        return f"Horario: {self.hora_inicio} - {self.hora_fin}"


# Modelo que representa los tratamientos que ofrece la clínica
class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del tratamiento
    descripcion_corta = models.CharField(max_length=200, blank=True, null=True)  # Breve descripción
    descripcion_larga = models.TextField(blank=True, null=True)  # Descripción más detallada
    descripcion_secundaria = models.TextField(blank=True, null=True)  # Descripción adicional opcional
    intervalo_minutos = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(10), MaxValueValidator(180)],
        help_text="Duración en minutos del tratamiento. Esto determina cuánto bloquea en el horario."
    )
    precio = models.CharField(max_length=20)  # Precio como string (puede incluir símbolo ₡)
    imagen = models.ImageField(upload_to='tratamientos/', blank=True, null=True)  # Imagen principal del tratamiento
    imagen_secundaria = models.ImageField(upload_to='tratamientos/', blank=True, null=True)  # Imagen adicional

    def __str__(self):
        return self.nombre


# Modelo que representa una cita agendada por un cliente
class Cita(models.Model):
    calendar_event_id = models.CharField(max_length=200, blank=True, null=True)  # ID del evento en Google Calendar
    nombre_cliente = models.CharField(max_length=100)  # Nombre de quien agenda
    contacto = models.CharField(max_length=100)  # Número de contacto (teléfono o WhatsApp)
    tratamiento = models.ForeignKey('Tratamiento', on_delete=models.CASCADE)  # Tratamiento elegido
    fecha = models.DateField()  # Fecha de la cita
    hora = models.TimeField()   # Hora de inicio
    comentarios = models.TextField(blank=True, null=True)  # Comentarios opcionales
    creada = models.DateTimeField(auto_now_add=True)  # Fecha y hora en que se registró la cita
    especialista = models.ForeignKey('Especialista', on_delete=models.SET_NULL, null=True, blank=True)  # Especialista asignado

    def __str__(self):
        return f"{self.nombre_cliente} - {self.tratamiento.nombre} - {self.fecha} {self.hora}"

    # Calcula la hora de finalización estimada de la cita
    def fin_estimado(self):
        from datetime import datetime, timedelta
        inicio_dt = datetime.combine(self.fecha, self.hora)
        fin_dt = inicio_dt + timedelta(minutes=self.tratamiento.intervalo_minutos)
        return fin_dt.time()


# Modelo que representa un bloqueo en el horario (ej: mantenimiento, feriado, etc.)
class BloqueoHorario(models.Model):
    fecha = models.DateField()           # Día bloqueado
    hora_inicio = models.TimeField()     # Hora en que inicia el bloqueo
    hora_fin = models.TimeField()        # Hora en que finaliza el bloqueo
    motivo = models.CharField(max_length=200, blank=True)  # Razón del bloqueo (opcional)

    class Meta:
        verbose_name = "Bloqueo de horario"
        verbose_name_plural = "Bloqueos de horario"

    def __str__(self):
        return f"Bloqueado: {self.fecha} de {self.hora_inicio} a {self.hora_fin}"


# Modelo que representa un especialista de la clínica
class Especialista(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del especialista
    especialidades = models.ManyToManyField('Tratamiento', related_name='especialistas', blank=True)  # Tratamientos que puede realizar

    def __str__(self):
        return self.nombre