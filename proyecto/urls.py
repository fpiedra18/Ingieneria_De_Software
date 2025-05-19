from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
<<<<<<< HEAD
from citas.pl.views import inicio

=======
from citas.views import inicio  # Opcional si se usa directamente alguna vista desde aquí
>>>>>>> origin/main

# Lista de rutas principales del proyecto
urlpatterns = [
    # Conecta todas las rutas definidas en 'citas/urls.py'
    path('', include('citas.urls')),

    # Ruta para acceder al panel de administración de Django
    path('admin/', admin.site.urls),
]

# Configuración para servir archivos multimedia (como imágenes) durante el desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
