from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agendar/', views.agendar_cita, name='agendar_cita'),
    path('agendar-protegido/', views.vista_protegida_agendar, name='agendar_protegido'),
    path('api/horarios/', views.obtener_horarios_disponibles, name='obtener_horarios'),
    path('guardar-cita/', views.guardar_cita_protegida, name='guardar_cita'),
    path('api/dias-disponibles/', views.dias_disponibles, name='dias_disponibles'),
    path('prueba/', views.prueba, name='prueba'),

    path('tratamiento/<int:tratamiento_id>/', views.detalle_tratamiento, name='detalle_tratamiento'),


]