
from django.http import JsonResponse
from ..models import Tratamiento, Cita, HorarioAtencion, BloqueoHorario, Especialista
from django.contrib import messages
from datetime import datetime, timedelta, date, time
from django.utils import timezone
from django.shortcuts import render,redirect, get_object_or_404
import re

def inicio(request):
    tratamientos = Tratamiento.objects.all()
    return render(request, 'inicio.html', {'tratamientos': tratamientos})

def detalle_tratamiento(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    return render(request, 'detalle_tratamiento.html', {'tratamiento': tratamiento})



def obtener_horarios_disponibles_para_tratamiento(tratamiento, fecha):
    horarios_disponibles = []
    especialistas = tratamiento.especialistas.all()
    horario = HorarioAtencion.objects.first()

    if not especialistas.exists() or not horario:
        return horarios_disponibles

    hora_actual = datetime.combine(fecha, horario.hora_inicio)
    hora_fin = datetime.combine(fecha, horario.hora_fin)

    while hora_actual + timedelta(minutes=tratamiento.intervalo_minutos) <= hora_fin:
        hora_inicio = hora_actual.time()
        hora_fin_estimada = (hora_actual + timedelta(minutes=tratamiento.intervalo_minutos)).time()

        bloqueo = BloqueoHorario.objects.filter(
            fecha=fecha,
            hora_inicio__lt=hora_fin_estimada,
            hora_fin__gt=hora_inicio
        ).exists()

        if not bloqueo:
            especialista_disponible = False
            for especialista in especialistas:
                conflicto = Cita.objects.filter(
                    fecha=fecha,
                    hora__lt=hora_fin_estimada,
                    hora__gte=hora_inicio,
                    especialista=especialista
                ).exists()
                if not conflicto:
                    especialista_disponible = True
                    break

            if especialista_disponible:
                horarios_disponibles.append(hora_inicio.strftime('%H:%M'))

        hora_actual += timedelta(minutes=tratamiento.intervalo_minutos)

    return horarios_disponibles



def vista_protegida_agendar(request):
    tratamientos = Tratamiento.objects.all()
    fecha_hoy = timezone.now().date().strftime('%Y-%m-%d')
    return render(request, 'agendar_protegido.html', {
        'tratamientos': tratamientos,
        'fecha_hoy': fecha_hoy
    })

def obtener_horarios_disponibles(request):
    tratamiento_id = request.GET.get('tratamiento_id')
    fecha_str = request.GET.get('fecha')

    if not tratamiento_id or not fecha_str:
        return JsonResponse({'horarios': []})

    try:
        tratamiento = Tratamiento.objects.get(id=tratamiento_id)
        especialistas = tratamiento.especialistas.all()
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        horario = HorarioAtencion.objects.first()

        if not horario:
            return JsonResponse({'horarios': []})

        hora_actual = datetime.combine(fecha, horario.hora_inicio)
        hora_fin = datetime.combine(fecha, horario.hora_fin)
        horarios_disponibles = []

        while hora_actual + timedelta(minutes=tratamiento.intervalo_minutos) <= hora_fin:
            hora_inicio = hora_actual.time()
            hora_fin_estimada = (hora_actual + timedelta(minutes=tratamiento.intervalo_minutos)).time()

            especialistas_disponibles = []
            for especialista in especialistas:
                conflicto = Cita.objects.filter(
                    fecha=fecha,
                    hora__lt=hora_fin_estimada,
                    hora__gte=hora_inicio,
                    especialista=especialista
                ).exists()
                if not conflicto:
                    especialistas_disponibles.append(especialista)

            bloqueo = BloqueoHorario.objects.filter(
                fecha=fecha,
                hora_inicio__lt=hora_fin_estimada,
                hora_fin__gt=hora_inicio
            ).exists()

            if especialistas_disponibles and not bloqueo:
                horarios_disponibles.append(hora_inicio.strftime('%H:%M'))

            hora_actual += timedelta(minutes=tratamiento.intervalo_minutos)

        return JsonResponse({'horarios': horarios_disponibles})

    except Exception:
        return JsonResponse({'horarios': []})



def guardar_cita_protegida(request):
    from ..calendar_sync import crear_evento_en_calendar

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        contacto = request.POST.get('contacto', '').strip()
        tratamiento_nombre = request.POST.get('tratamiento', '').strip()
        fecha_str = request.POST.get('fecha', '').strip()
        hora_str = request.POST.get('hora', '').strip()

        if not nombre or not contacto or not tratamiento_nombre or not fecha_str or not hora_str:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('agendar_protegido')

        patron_telefono = re.compile(r'^(?:\d{4}-\d{4}|\d{8})$')
        if not patron_telefono.match(contacto):
            messages.error(request, 'El número de WhatsApp debe tener 8 dígitos (ejemplo: 8888-8888).')
            return redirect('agendar_protegido')

        patron_nombre = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]{3,}$')
        if not patron_nombre.match(nombre):
            messages.error(request, 'El nombre debe contener al menos 3 letras y no incluir números ni símbolos.')
            return redirect('agendar_protegido')

        try:
            tratamiento = Tratamiento.objects.get(nombre=tratamiento_nombre)
            especialistas = tratamiento.especialistas.all()

            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora = datetime.strptime(hora_str, '%H:%M').time()

            ahora = timezone.now()
            fecha_hora_cita = timezone.make_aware(datetime.combine(fecha, hora))
            if fecha_hora_cita - ahora < timedelta(minutes=30):
                messages.error(request, 'Las citas deben agendarse al menos con 30 minutos de anticipación.')
                return redirect('agendar_protegido')

            hora_inicio_dt = datetime.combine(fecha, hora)
            hora_fin_dt = hora_inicio_dt + timedelta(minutes=tratamiento.intervalo_minutos)

            especialista_asignado = None
            for especialista in especialistas:
                conflicto = Cita.objects.filter(
                    fecha=fecha,
                    hora__lt=hora_fin_dt.time(),
                    hora__gte=hora,
                    especialista=especialista
                ).exists()
                if not conflicto:
                    especialista_asignado = especialista
                    break

            if not especialista_asignado:
                messages.error(request, 'No hay especialistas disponibles para ese horario.')
                return redirect('agendar_protegido')

            bloqueo = BloqueoHorario.objects.filter(
                fecha=fecha,
                hora_inicio__lt=hora_fin_dt.time(),
                hora_fin__gt=hora
            ).exists()

            if bloqueo:
                messages.error(request, 'Ese horario está bloqueado.')
                return redirect('agendar_protegido')

            nueva_cita = Cita.objects.create(
                nombre_cliente=nombre,
                contacto=contacto,
                tratamiento=tratamiento,
                especialista=especialista_asignado,
                fecha=fecha,
                hora=hora,
            )
            
            try:
                event_id = crear_evento_en_calendar(nombre, tratamiento.nombre, fecha, hora, contacto, especialista_asignado.nombre)
                if event_id:
                    nueva_cita.calendar_event_id = event_id
                    nueva_cita.save()
            except Exception as e:
                print("❌ Error al crear evento en Google Calendar:", e)
                messages.warning(request, 'Cita guardada, pero hubo un problema al sincronizar con el calendario.')

            return render(request, 'gracias.html')

        except Tratamiento.DoesNotExist:
            messages.error(request, 'Tratamiento no encontrado.')
            return redirect('agendar_protegido')
        except Exception as e:
            print("🛑 Error inesperado al guardar cita:", e)
            messages.error(request, 'Error al guardar la cita.')
            return redirect('agendar_protegido')



        
def dias_disponibles(request):
    tratamiento_id = request.GET.get('tratamiento_id')
    if not tratamiento_id:
        return JsonResponse({'dias': []})

    try:
        tratamiento = Tratamiento.objects.get(id=tratamiento_id)
    except Tratamiento.DoesNotExist:
        return JsonResponse({'dias': []})

    dias_disponibles = []
    hoy = timezone.now().date()
    rango_dias = 30  # próximos 30 días

    for i in range(rango_dias):
        fecha = hoy + timedelta(days=i)
        horarios = obtener_horarios_disponibles_para_tratamiento(tratamiento, fecha)
        if horarios:
            dias_disponibles.append(fecha.strftime('%Y-%m-%d'))

    return JsonResponse({'dias': dias_disponibles})

