from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# --------------------------------------------------------------------
# MODELO: HorarioAtencion
# Define las horas generales de apertura y cierre de la clínica
# --------------------------------------------------------------------
class HorarioAtencion(models.Model):
    hora_inicio = models.TimeField(default='07:00')  # Hora en que inicia la atención
    hora_fin = models.TimeField(default='19:00')     # Hora en que finaliza la atención

    class Meta:
        verbose_name = "Horario de atención"
        verbose_name_plural = "Horario de atención"

    def __str__(self):
        return f"Horario: {self.hora_inicio} - {self.hora_fin}"

# --------------------------------------------------------------------
# MODELO: Tratamiento
# Representa los servicios estéticos ofrecidos por la clínica
# Incluye duración, precio, descripciones e imágenes
# --------------------------------------------------------------------
class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion_corta = models.CharField(max_length=200, blank=True, null=True)
    descripcion_larga = models.TextField(blank=True, null=True)
    descripcion_secundaria = models.TextField(blank=True, null=True)  # Usada para diseño o info adicional
    intervalo_minutos = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(10), MaxValueValidator(180)],
        help_text="Duración en minutos del tratamiento. Esto determina cuánto bloquea en el horario."
    )
    precio = models.CharField(max_length=20)  # Precio formateado como string (ejemplo: '₡25,000')
    imagen = models.ImageField(upload_to='tratamientos/', blank=True, null=True)
    imagen_secundaria = models.ImageField(upload_to='tratamientos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

# --------------------------------------------------------------------
# MODELO: Cita
# Representa una reserva de tratamiento realizada por un cliente
# Se enlaza con Google Calendar mediante el campo calendar_event_id
# --------------------------------------------------------------------
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

    # Calcula la hora de finalización estimada de la cita
    def fin_estimado(self):
        """
        Calcula la hora estimada de finalización de la cita
        según la duración del tratamiento.
        """
        from datetime import datetime, timedelta
        inicio_dt = datetime.combine(self.fecha, self.hora)
        fin_dt = inicio_dt + timedelta(minutes=self.tratamiento.intervalo_minutos)
        return fin_dt.time()

# --------------------------------------------------------------------
# MODELO: BloqueoHorario
# Permite bloquear rangos de horario para mantenimiento u otros motivos
# --------------------------------------------------------------------
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

# --------------------------------------------------------------------
# MODELO: Especialista
# Representa a los profesionales que ofrecen tratamientos
# Se vincula con los tratamientos mediante una relación ManyToMany
# --------------------------------------------------------------------
class Especialista(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del especialista
    especialidades = models.ManyToManyField('Tratamiento', related_name='especialistas', blank=True)  # Tratamientos que puede realizar

    def __str__(self):
        return self.nombre