from citas.models import Tratamiento, Cita, BloqueoHorario

def obtener_tratamiento_por_nombre(nombre):
    """
    Recupera una instancia de Tratamiento a partir de su nombre.

    Parámetros:
    ----------
    nombre : str
        Nombre exacto del tratamiento que se desea buscar.

    Retorna:
    -------
    Tratamiento
        Objeto del modelo Tratamiento que coincide con el nombre especificado.

    Excepciones:
    ----------
    Lanza Tratamiento.DoesNotExist si no se encuentra un tratamiento con ese nombre.
    """
    return Tratamiento.objects.get(nombre=nombre)


def crear_cita(**kwargs):
    """
    Crea y guarda una nueva instancia del modelo Cita en la base de datos.

    Parámetros:
    ----------
    **kwargs : dict
        Argumentos clave necesarios para la creación de una cita. Debe incluir:
        - nombre_cliente
        - contacto
        - tratamiento (instancia)
        - especialista (instancia)
        - fecha
        - hora

    Retorna:
    -------
    Cita
        Objeto de tipo Cita recién creado y guardado en la base de datos.
    """
    return Cita.objects.create(**kwargs)


def hay_bloqueo(fecha, hora_inicio, hora_fin):
    """
    Verifica si existe un bloqueo de horario en una fecha y rango de horas específico.

    Parámetros:
    ----------
    fecha : date
        Día en el que se desea agendar la cita.
    hora_inicio : time
        Hora de inicio del rango a verificar.
    hora_fin : time
        Hora de fin del rango a verificar.

    Retorna:
    -------
    bool
        True si hay un bloqueo que se superpone con el rango dado, False en caso contrario.
    """
    return BloqueoHorario.objects.filter(
        fecha=fecha,
        hora_inicio__lt=hora_fin,
        hora_fin__gt=hora_inicio
    ).exists()
