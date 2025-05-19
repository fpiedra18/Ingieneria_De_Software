from citas.models import Tratamiento, Cita, BloqueoHorario

def obtener_tratamiento_por_nombre(nombre):
    return Tratamiento.objects.get(nombre=nombre)

def crear_cita(**kwargs):
    return Cita.objects.create(**kwargs)

def hay_bloqueo(fecha, hora_inicio, hora_fin):
    return BloqueoHorario.objects.filter(
        fecha=fecha,
        hora_inicio__lt=hora_fin,
        hora_fin__gt=hora_inicio
    ).exists()
