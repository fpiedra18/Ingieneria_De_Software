from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# -----------------------------------------------------------------------------
# Módulo de sincronización con Google Calendar
# Contiene funciones para crear y eliminar eventos automáticamente
# utilizando las credenciales autorizadas del usuario.
# -----------------------------------------------------------------------------

def crear_evento_en_calendar(nombre, tratamiento, fecha, hora, contacto, especialista):
    """
    Crea un evento en Google Calendar con los detalles de una cita agendada.

    Parámetros:
        nombre (str): Nombre del cliente.
        tratamiento (str): Nombre del tratamiento reservado.
        fecha (datetime.date): Fecha programada para la cita.
        hora (datetime.time): Hora de inicio de la cita.
        contacto (str): Número de contacto del cliente.
        especialista (str): Nombre del especialista asignado.

    Retorna:
        str | None: ID del evento creado en Google Calendar o None si falla.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']  # Permisos requeridos

    # Verifica que todos los parámetros requeridos estén presentes
    if not all([nombre, tratamiento, fecha, hora, contacto, especialista]):
        print("❌ Faltan datos necesarios para crear el evento en Calendar.")
        return None

    creds = None
    token_path = os.path.join('credentials', 'token.json')  # Ruta al token de acceso

    # Intenta cargar las credenciales desde el archivo token.json
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Se construye el cliente para acceder a la API de Google Calendar
    service = build('calendar', 'v3', credentials=creds)

    # Define hora de inicio y fin del evento
    hora_inicio = datetime.datetime.combine(fecha, hora)
    duracion = getattr(tratamiento, 'intervalo_minutos', 60) if hasattr(tratamiento, 'intervalo_minutos') else 60
    hora_fin = hora_inicio + datetime.timedelta(minutes=duracion)

    # Cuerpo del evento con formato y detalles
    descripcion = (
        f"📆 Fecha: {fecha.strftime('%d/%m/%Y')}\n"
        f"🕒 Hora: {hora.strftime('%H:%M')}\n"
        f"👤 Cliente: {nombre}\n"
        f"📱 WhatsApp: {contacto}\n"
        f"💼 Especialista: {especialista}\n"
        f"💬 Reservado desde NaturaClick"
    )

    # Estructura del evento a enviar a Google Calendar
    evento = {
        'summary': f'{tratamiento} | Cliente: {nombre} | {especialista}',  # Título del evento
        'description': descripcion,  # Descripción completa
        'start': {
            'dateTime': hora_inicio.isoformat(),
            'timeZone': 'America/Costa_Rica',
        },
        'end': {
            'dateTime': hora_fin.isoformat(),
            'timeZone': 'America/Costa_Rica',
        },
        'location': 'Clínica Natura, Grecia, Costa Rica',
        'colorId': None,  # Puede asignarse un color si se desea
    }

    # Intenta insertar el evento en el calendario
    try:
        evento_creado = service.events().insert(calendarId='primary', body=evento).execute()
        print(f"✅ Evento creado en Google Calendar: {evento_creado.get('htmlLink')}")
        return evento_creado.get('id')
    except Exception as e:
        print(f"❌ Error al crear evento en Google Calendar: {e}")
        return None


def eliminar_evento_de_calendar(event_id):
    """
    Elimina un evento de Google Calendar utilizando su ID.

    Parámetros:
        event_id (str): ID único del evento a eliminar.

    Retorna:
        None
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    token_path = os.path.join('credentials', 'token.json')

    # Carga credenciales desde el archivo
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Construye el servicio de calendar
    service = build('calendar', 'v3', credentials=creds)

    # Intenta eliminar el evento
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print("✅ Evento eliminado correctamente de Google Calendar.")
    except Exception as e:
        print(f"❌ Error al eliminar evento de Google Calendar: {e}")