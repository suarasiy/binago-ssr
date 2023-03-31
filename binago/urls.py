from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    dashboard
)

urlpatterns = [
    path('__reload__/', include('django_browser_reload.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include([
        path('overview/', include('Dashboard.urls')),
        # path('organizers/', include('Organizers.urls')),
        path('associations/', include('Associations.urls')),
        path('events/', include('Events.urls')),
    ]))
]

# media
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
