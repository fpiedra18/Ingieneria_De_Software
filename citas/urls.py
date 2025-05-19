# Importación de funciones necesarias de Django
from django.urls import path
from . import views  # Importa las vistas del archivo views.py de la misma app

# Definición de las rutas (URL patterns) de la aplicación
urlpatterns = [
    # Ruta raíz (inicio del sitio)
    path('', views.inicio, name='inicio'),

    # Página para agendar una cita desde la vista pública
    path('agendar/', views.agendar_cita, name='agendar_cita'),

    # Página para agendar desde la vista protegida (acceso restringido o con link privado)
    path('agendar-protegido/', views.vista_protegida_agendar, name='agendar_protegido'),

    # Endpoint API para obtener horarios disponibles por tratamiento y fecha
    path('api/horarios/', views.obtener_horarios_disponibles, name='obtener_horarios'),

    # Ruta para guardar una cita desde el formulario protegido
    path('guardar-cita/', views.guardar_cita_protegida, name='guardar_cita'),

    # Endpoint API para obtener días disponibles en un mes
    path('api/dias-disponibles/', views.dias_disponibles, name='dias_disponibles'),

    # Ruta de prueba (puede usarse para testear componentes visuales o scripts)
    path('prueba/', views.prueba, name='prueba'),

    # Vista de detalle de un tratamiento específico, recibe ID por URL
    path('tratamiento/<int:tratamiento_id>/', views.detalle_tratamiento, name='detalle_tratamiento'),
]
