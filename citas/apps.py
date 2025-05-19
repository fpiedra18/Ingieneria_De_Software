from django.apps import AppConfig

class CitasConfig(AppConfig):
    """
    Configuración principal de la aplicación 'citas'.
    
    Esta clase define el comportamiento de inicialización de la app dentro del proyecto Django,
    especificando el nombre del módulo y el tipo de clave primaria predeterminada para los modelos.

    Atributos:
        default_auto_field (str): Define el tipo de campo automático para claves primarias.
        name (str): Nombre de la aplicación dentro del proyecto.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'citas'
