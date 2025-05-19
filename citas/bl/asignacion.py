from datetime import datetime, timedelta
from citas.models import Cita

def asignar_especialista_disponible(tratamiento, fecha, hora):
    especialistas = tratamiento.especialistas.all()
    hora_inicio_dt = datetime.combine(fecha, hora)
    hora_fin_dt = hora_inicio_dt + timedelta(minutes=tratamiento.intervalo_minutos)

    for especialista in especialistas:
        conflicto = Cita.objects.filter(
            fecha=fecha,
            hora__lt=hora_fin_dt.time(),
            hora__gte=hora,
            especialista=especialista
        ).exists()
        if not conflicto:
            return especialista
    return None
