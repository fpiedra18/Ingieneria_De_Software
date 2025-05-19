from datetime import datetime, timedelta
from citas.models import BloqueoHorario, Cita, HorarioAtencion

def obtener_horarios_disponibles_para_tratamiento(tratamiento, fecha):
    horarios_disponibles = []
    especialistas = tratamiento.especialistas.all()
    horario = HorarioAtencion.objects.first()

    if not especialistas.exists() or not horario:
        return horarios_disponibles

    hora_actual = datetime.combine(fecha, horario.hora_inicio)
    hora_fin = datetime.combine(fecha, horario.hora_fin)

    while hora_actual + timedelta(minutes=tratamiento.intervalo_minutos) <= hora_fin:
        hora_inicio = hora_actual.time()
        hora_fin_estimada = (hora_actual + timedelta(minutes=tratamiento.intervalo_minutos)).time()

        bloqueo = BloqueoHorario.objects.filter(
            fecha=fecha,
            hora_inicio__lt=hora_fin_estimada,
            hora_fin__gt=hora_inicio
        ).exists()

        if not bloqueo:
            especialista_disponible = False
            for especialista in especialistas:
                conflicto = Cita.objects.filter(
                    fecha=fecha,
                    hora__lt=hora_fin_estimada,
                    hora__gte=hora_inicio,
                    especialista=especialista
                ).exists()
                if not conflicto:
                    especialista_disponible = True
                    break

            if especialista_disponible:
                horarios_disponibles.append(hora_inicio.strftime('%H:%M'))

        hora_actual += timedelta(minutes=tratamiento.intervalo_minutos)

    return horarios_disponibles
