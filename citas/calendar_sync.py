from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def crear_evento_en_calendar(nombre, tratamiento, fecha, hora, contacto):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    hora_inicio = datetime.datetime.combine(fecha, hora)
    hora_fin = hora_inicio + datetime.timedelta(minutes=60)  # Personalizable por tratamiento

    descripcion = f"""
📆 Fecha: {fecha.strftime('%d/%m/%Y')}
🕒 Hora: {hora.strftime('%H:%M')}
👤 Cliente: {nombre}
📱 WhatsApp: {contacto}
💬 Reservado desde NaturaClick
"""

    evento = {
        'summary': f'{tratamiento} | Cliente: {nombre}',
        'description': descripcion.strip(),
        'start': {
            'dateTime': hora_inicio.isoformat(),
            'timeZone': 'America/Costa_Rica',
        },
        'end': {
            'dateTime': hora_fin.isoformat(),
            'timeZone': 'America/Costa_Rica',
        },
        'location': 'Clínica Natura, Grecia, Costa Rica',
        'colorId': '11',  # Podés mapear esto luego por tratamiento si querés
    }

    try:
        evento = service.events().insert(calendarId='primary', body=evento).execute()
        print(f"✅ Evento creado en Google Calendar: {evento.get('htmlLink')}")
        return evento.get('id')  # ¡IMPORTANTE! Para poder borrarlo después
    except Exception as e:
        print(f"❌ Error al crear evento en Google Calendar: {e}")
        return None
def eliminar_evento_de_calendar(event_id):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print("Evento eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el evento: {e}")
#OOOKOOKOKOOKOKOK