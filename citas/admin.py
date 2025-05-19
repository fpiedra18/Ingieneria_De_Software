from django.contrib import admin
from .models import Tratamiento, Cita, HorarioAtencion, BloqueoHorario, Especialista
from .calendar_sync import eliminar_evento_de_calendar
from .models import Especialista

# ----------------------------------------------------------------------------------
# Configuración del administrador de Django para modelos personalizados del sistema
# ----------------------------------------------------------------------------------
 
@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'intervalo_minutos', 'precio')  # Columnas visibles en la lista
    fields = (
        'nombre', 'precio', 'intervalo_minutos', 
        'descripcion_larga', 'descripcion_secundaria', 
        'imagen', 'imagen_secundaria'
    )  # Campos visibles en el formulario

# Configuración del panel de administración para el modelo Especialista
@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Muestra solo el nombre en la lista
    search_fields = ('nombre',)  # Permite buscar por nombre
    filter_horizontal = ('especialidades',)  # Usa selector horizontal para relaciones many-to-many

# Configuración del panel de administración para el modelo Cita
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'tratamiento', 'especialista', 'fecha', 'hora')  # Columnas visibles
    list_filter = ('fecha', 'tratamiento', 'especialista')  # Filtros en el sidebar
    search_fields = ('nombre_cliente', 'contacto')  # Barra de búsqueda

    # Al eliminar una cita, intenta eliminar también el evento de Google Calendar
    def delete_model(self, request, obj):
        if obj.calendar_event_id:
            try:
                eliminar_evento_de_calendar(obj.calendar_event_id)
            except Exception as e:
                print(f"⚠️ No se pudo eliminar evento en Calendar: {e}")
        super().delete_model(request, obj)

    # Al eliminar múltiples citas al mismo tiempo, también elimina los eventos del Calendar
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.calendar_event_id:
                try:
                    eliminar_evento_de_calendar(obj.calendar_event_id)
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar evento en Calendar: {e}")
        super().delete_queryset(request, queryset)

# Configuración del panel de administración para Horario de Atención
@admin.register(HorarioAtencion)
class HorarioAtencionAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio', 'hora_fin')  # Muestra el rango de atención

# Configuración del panel de administración para Bloqueos de Horario
@admin.register(BloqueoHorario)
class BloqueoHorarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'hora_fin', 'motivo')  # Columnas visibles
    list_filter = ('fecha',)  # Filtro por fecha
    search_fields = ('motivo',)  # Búsqueda por motivo