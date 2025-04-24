
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from citas.views import inicio


urlpatterns = [
    
     path('', include('citas.urls')),  # ← esto conecta tu app
    path('admin/', admin.site.urls),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
