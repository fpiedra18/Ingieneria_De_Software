from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# -----------------------------------------------------------------------------
# Funciones para sincronizar con Google Calendar
# -----------------------------------------------------------------------------

def crear_evento_en_calendar(nombre, tratamiento, fecha, hora, contacto, especialista):
    """
    Crea un evento en el calendario de Google con la información de la cita.

    Parámetros:
    - nombre (str): Nombre del cliente.
    - tratamiento (str): Nombre del tratamiento reservado.
    - fecha (date): Fecha de la cita.
    - hora (time): Hora de inicio de la cita.
    - contacto (str): Número de WhatsApp o contacto.
    - especialista (str): Nombre del especialista asignado.

    Retorna:
    - id del evento en Google Calendar (str) o None si ocurre un error.
    """
    # Alcances necesarios para Calendar API
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Validar datos obligatorios
    if not all([nombre, tratamiento, fecha, hora, contacto, especialista]):
        print("❌ Faltan datos necesarios para crear el evento en Calendar.")
        return None

    creds = None
    token_path = os.path.join('credentials', 'token.json')
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    # Calcular hora de inicio y fin (ajustar duración si es necesario)
    hora_inicio = datetime.datetime.combine(fecha, hora)
    # Podemos usar un bloque por defecto de 60 minutos o extendido si se pasa
    duracion = getattr(tratamiento, 'intervalo_minutos', 60) if hasattr(tratamiento, 'intervalo_minutos') else 60
    hora_fin = hora_inicio + datetime.timedelta(minutes=duracion)

    # Descripción detallada del evento
    descripcion = (
        f"📆 Fecha: {fecha.strftime('%d/%m/%Y')}\n"
        f"🕒 Hora: {hora.strftime('%H:%M')}\n"
        f"👤 Cliente: {nombre}\n"
        f"📱 WhatsApp: {contacto}\n"
        f"💼 Especialista: {especialista}\n"
        f"💬 Reservado desde NaturaClick"
    )

    evento = {
        'summary': f'{tratamiento} | Cliente: {nombre} | {especialista}',
        'description': descripcion,
        'start': {
            'dateTime': hora_inicio.isoformat(),
            'timeZone': 'America/Costa_Rica',
        },
        'end': {
            'dateTime': hora_fin.isoformat(),
            'timeZone': 'America/Costa_Rica',
        },
        'location': 'Clínica Natura, Grecia, Costa Rica',
        'colorId': None,  # Se asignará automáticamente o podrá mapearse dinámicamente
    }

    try:
        evento_creado = service.events().insert(calendarId='primary', body=evento).execute()
        print(f"✅ Evento creado en Google Calendar: {evento_creado.get('htmlLink')}")
        return evento_creado.get('id')
    except Exception as e:
        print(f"❌ Error al crear evento en Google Calendar: {e}")
        return None


def eliminar_evento_de_calendar(event_id):
    """
    Elimina un evento existente de Google Calendar por su ID.

    Parámetros:
    - event_id (str): ID del evento a eliminar.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    token_path = os.path.join('credentials', 'token.json')
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print("✅ Evento eliminado correctamente de Google Calendar.")
    except Exception as e:
        print(f"❌ Error al eliminar evento de Google Calendar: {e}")
