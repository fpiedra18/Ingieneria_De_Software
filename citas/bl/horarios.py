from datetime import datetime, timedelta
from citas.models import BloqueoHorario, Cita, HorarioAtencion

def obtener_horarios_disponibles_para_tratamiento(tratamiento, fecha):
    """
    Retorna una lista de horarios disponibles para agendar un tratamiento en una fecha específica.

    Esta función toma en cuenta:
    - El horario de atención definido.
    - Los bloqueos de horario (por mantenimiento, eventos especiales, etc.).
    - La disponibilidad de especialistas (según otras citas ya agendadas).

    Parámetros:
    - tratamiento: instancia del modelo Tratamiento (incluye duración y especialistas asociados).
    - fecha: objeto date correspondiente al día que se desea consultar.

    Retorna:
    - Lista de strings en formato 'HH:MM' que representan los horarios disponibles para agendar.
    """
    horarios_disponibles = []
    especialistas = tratamiento.especialistas.all()
    horario = HorarioAtencion.objects.first()

    # Si no hay especialistas asignados o no hay un horario definido, retornar lista vacía
    if not especialistas.exists() or not horario:
        return horarios_disponibles

    # Inicializar hora actual y fin del día laboral
    hora_actual = datetime.combine(fecha, horario.hora_inicio)
    hora_fin = datetime.combine(fecha, horario.hora_fin)

    # Recorrer bloques de tiempo válidos en el rango horario
    while hora_actual + timedelta(minutes=tratamiento.intervalo_minutos) <= hora_fin:
        hora_inicio = hora_actual.time()
        hora_fin_estimada = (hora_actual + timedelta(minutes=tratamiento.intervalo_minutos)).time()

        # Verificar si ese bloque está bloqueado por un evento especial
        bloqueo = BloqueoHorario.objects.filter(
            fecha=fecha,
            hora_inicio__lt=hora_fin_estimada,
            hora_fin__gt=hora_inicio
        ).exists()

        # Si no está bloqueado, buscar si hay al menos un especialista disponible
        if not bloqueo:
            especialista_disponible = False
            for especialista in especialistas:
                conflicto = Cita.objects.filter(
                    fecha=fecha,
                    hora__lt=hora_fin_estimada,
                    hora__gte=hora_inicio,
                    especialista=especialista
                ).exists()

                # Si no hay conflicto con ese especialista, marcar como disponible y salir del loop
                if not conflicto:
                    especialista_disponible = True
                    break

            # Si al menos un especialista está libre, agregar el horario a la lista
            if especialista_disponible:
                horarios_disponibles.append(hora_inicio.strftime('%H:%M'))

        # Avanzar al siguiente bloque de tiempo
        hora_actual += timedelta(minutes=tratamiento.intervalo_minutos)

    return horarios_disponibles
