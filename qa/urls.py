from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('i18n/setlang', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('device.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('device/', include('device.urls')),
    path('firmware/', include('firmware.urls')),
    path('docum/', include('docum.urls')),
    path('testplan/', include('testplan.urls')),
    path('pattern/', include('testplan_pattern.urls')),
    path('redmine/', include('redmine.urls')),
    path('paper/', include('paper.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
