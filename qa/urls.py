from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('i18n/setlang', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('device.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('device/', include('device.urls')),
    path('docum/', include('docum.urls')),
    path('testplan/', include('testplan.urls')),
    path('redmine/', include('redmine.urls')),
    path('paper/', include('paper.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('device.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('device/', include('device.urls')),
    prefix_default_language=False,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''