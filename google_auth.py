from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Ámbito de permisos que solicitaremos: acceso completo al calendario de Google
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Crea el flujo de autenticación leyendo las credenciales de cliente
# El archivo 'credentials/credentials.json' debe contener tu Client ID y Client Secret.
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials/credentials.json',  # Ruta al JSON con tus credenciales de OAuth 2.0
    SCOPES                           # Lista de scopes que pedimos
)

# Inicia un servidor web local en un puerto aleatorio para completar el OAuth
# Abre automáticamente el navegador para que el usuario autorice la app
creds = flow.run_local_server(port=0)

# Una vez autorizado, 'creds' contiene el token de acceso y el de refresco
# Lo guardamos en un archivo para reutilizarlo sin tener que autorizar de nuevo
with open('credentials/token.json', 'w') as token:
    token.write(creds.to_json())
