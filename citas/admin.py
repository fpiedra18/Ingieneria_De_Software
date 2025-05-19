
from django.contrib import admin
from .models import Tratamiento, Cita, HorarioAtencion, BloqueoHorario
from .calendar_sync import eliminar_evento_de_calendar
from .models import Especialista

# ----------------------------------------------------------------------------------
# Configuración del administrador de Django para modelos personalizados del sistema
# ----------------------------------------------------------------------------------
 
@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'intervalo_minutos', 'precio')
    fields = ('nombre', 'precio', 'intervalo_minutos', 'descripcion_larga', 'descripcion_secundaria', 'imagen', 'imagen_secundaria')
   
@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    filter_horizontal = ('especialidades',)  # ✅ Aquí sí.


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'tratamiento','especialista', 'fecha', 'hora')
    list_filter = ('fecha', 'tratamiento','especialista')
    search_fields = ('nombre_cliente', 'contacto')

    def delete_model(self, request, obj):
        if obj.calendar_event_id:
            try:
                eliminar_evento_de_calendar(obj.calendar_event_id)
            except Exception as e:
                print(f"⚠️ No se pudo eliminar evento en Calendar: {e}")
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.calendar_event_id:
                try:
                    eliminar_evento_de_calendar(obj.calendar_event_id)
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar evento en Calendar: {e}")
        super().delete_queryset(request, queryset)

@admin.register(HorarioAtencion)
class HorarioAtencionAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio', 'hora_fin')

@admin.register(BloqueoHorario)
class BloqueoHorarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'hora_fin', 'motivo')
    list_filter = ('fecha',)
    search_fields = ('motivo',)
