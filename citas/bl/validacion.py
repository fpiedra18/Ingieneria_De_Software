import re
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages

def validar_datos_basicos(request, nombre, contacto, tratamiento, fecha_str, hora_str):
    if not nombre or not contacto or not tratamiento or not fecha_str or not hora_str:
        messages.error(request, 'Todos los campos son obligatorios.')
        return False

    patron_telefono = re.compile(r'^(?:\d{4}-\d{4}|\d{8})$')
    if not patron_telefono.match(contacto):
        messages.error(request, 'El número de WhatsApp debe tener 8 dígitos (ejemplo: 8888-8888).')
        return False

    patron_nombre = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]{3,}$')
    if not patron_nombre.match(nombre):
        messages.error(request, 'El nombre debe contener al menos 3 letras y no incluir números ni símbolos.')
        return False

    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    hora = datetime.strptime(hora_str, '%H:%M').time()
    fecha_hora_cita = timezone.make_aware(datetime.combine(fecha, hora))
    if fecha_hora_cita - timezone.now() < timedelta(minutes=30):
        messages.error(request, 'Las citas deben agendarse al menos con 30 minutos de anticipación.')
        return False

    return True
