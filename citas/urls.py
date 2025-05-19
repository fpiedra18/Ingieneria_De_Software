from django.urls import path
from citas.pl import views  # Se importan las vistas desde la capa de presentación (PL)




# ----------------------------------------------------------------------------------
# Archivo de rutas (urls.py) de la aplicación 'citas'
# Define las URL que se pueden acceder y qué vista las va a manejar.
# Cada path incluye una ruta, una vista asociada y un nombre para referenciarla.
# ----------------------------------------------------------------------------------

urlpatterns = [
    # Ruta principal de la app: muestra los tratamientos disponibles
    path('', views.inicio, name='inicio'),

    # Ruta protegida para agendar una cita (solo accesible por link directo o validación previa)
    path('agendar-protegido/', views.vista_protegida_agendar, name='agendar_protegido'),

    # Endpoint API: devuelve los horarios disponibles para un tratamiento y fecha dados
    path('api/horarios/', views.obtener_horarios_disponibles, name='obtener_horarios'),

    # Ruta que procesa y guarda una nueva cita en el sistema
    path('guardar-cita/', views.guardar_cita_protegida, name='guardar_cita'),

    # Endpoint API: devuelve los días disponibles para un tratamiento durante los próximos 30 días
    path('api/dias-disponibles/', views.dias_disponibles, name='dias_disponibles'),

    # Ruta para ver los detalles de un tratamiento específico, según su ID
    path('tratamiento/<int:tratamiento_id>/', views.detalle_tratamiento, name='detalle_tratamiento'),
]

