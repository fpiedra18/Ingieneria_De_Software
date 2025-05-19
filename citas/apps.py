from django.apps import AppConfig

# Configuración principal de la aplicación "citas"
class CitasConfig(AppConfig):
    # Define el tipo de campo automático para claves primarias (BigAutoField por defecto)
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la aplicación (debe coincidir con el nombre del directorio)
    name = 'citas'
