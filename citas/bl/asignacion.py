from datetime import datetime, timedelta
from citas.models import Cita

def asignar_especialista_disponible(tratamiento, fecha, hora):
    """
    Asigna automáticamente un especialista disponible para un tratamiento en una fecha y hora específicas.

    Parámetros:
    - tratamiento: instancia del modelo Tratamiento que contiene la duración y la relación con los especialistas.
    - fecha: objeto date que representa el día solicitado.
    - hora: objeto time que representa la hora solicitada.

    Retorna:
    - El primer especialista disponible que no tenga conflicto en ese horario.
    - None si no hay ningún especialista disponible.
    """
    # Obtener todos los especialistas que pueden aplicar este tratamiento
    especialistas = tratamiento.especialistas.all()

    # Calcular la hora final estimada de la cita según la duración del tratamiento
    hora_inicio_dt = datetime.combine(fecha, hora)
    hora_fin_dt = hora_inicio_dt + timedelta(minutes=tratamiento.intervalo_minutos)

    # Recorrer especialistas para verificar disponibilidad
    for especialista in especialistas:
        # Verifica si el especialista tiene un conflicto en el horario solicitado
        conflicto = Cita.objects.filter(
            fecha=fecha,
            hora__lt=hora_fin_dt.time(),
            hora__gte=hora,
            especialista=especialista
        ).exists()

        # Si no hay conflicto, se retorna este especialista como disponible
        if not conflicto:
            return especialista

    # Si todos tienen conflicto, se retorna None
    return None
