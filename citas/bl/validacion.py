import re
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages

def validar_datos_basicos(request, nombre, contacto, tratamiento, fecha_str, hora_str):
    """
    Valida los datos ingresados por el usuario antes de agendar una cita.

    Esta función verifica que:
    - Todos los campos requeridos estén presentes.
    - El formato del nombre y el contacto sea correcto.
    - La cita se agende con al menos 30 minutos de anticipación.

    Parámetros:
    ----------
    request : HttpRequest
        La solicitud HTTP actual, utilizada para mostrar mensajes de error al usuario.
    nombre : str
        Nombre del cliente que agenda la cita.
    contacto : str
        Número de contacto del cliente (debe tener 8 dígitos).
    tratamiento : str
        Nombre del tratamiento solicitado.
    fecha_str : str
        Fecha de la cita en formato 'YYYY-MM-DD'.
    hora_str : str
        Hora de la cita en formato 'HH:MM'.

    Retorna:
    -------
    bool
        True si todos los datos son válidos, False en caso contrario. Si es False, se muestran mensajes de error al usuario.
    """

    # Verificar que todos los campos estén presentes
    if not nombre or not contacto or not tratamiento or not fecha_str or not hora_str:
        messages.error(request, 'Todos los campos son obligatorios.')
        return False

    # Validar formato del número de WhatsApp (8 dígitos, con o sin guion)
    patron_telefono = re.compile(r'^(?:\d{4}-\d{4}|\d{8})$')
    if not patron_telefono.match(contacto):
        messages.error(request, 'El número de WhatsApp debe tener 8 dígitos (ejemplo: 8888-8888).')
        return False

    # Validar que el nombre tenga al menos 3 letras y no contenga símbolos o números
    patron_nombre = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]{3,}$')
    if not patron_nombre.match(nombre):
        messages.error(request, 'El nombre debe contener al menos 3 letras y no incluir números ni símbolos.')
        return False

    # Verificar que la cita se agende con al menos 30 minutos de anticipación
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    hora = datetime.strptime(hora_str, '%H:%M').time()
    fecha_hora_cita = timezone.make_aware(datetime.combine(fecha, hora))
    if fecha_hora_cita - timezone.now() < timedelta(minutes=30):
        messages.error(request, 'Las citas deben agendarse al menos con 30 minutos de anticipación.')
        return False

    return True
