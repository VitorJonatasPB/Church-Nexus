from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls), # Mudando o admin de volta para /admin/ para liberar o / para o painel custom
    path('secretaria/', include('apps.secretaria.urls')), 
    path('eventos/', include('apps.eventos.urls')), 
    path('tesouraria/', include('apps.tesouraria.urls')), 
    path('', include('core.urls')), # O frontend core assume a raiz do site
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)