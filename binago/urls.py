from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler404, handler403, handler500
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    dashboard, settings_profile, signout, handle_403, handle_404, handle_500
)

from authentication.views import signin, register, verify_account, request_verify_account

if TYPE_CHECKING:
    from typing import Any


urlpatterns = [
    path('__reload__/', include('django_browser_reload.urls')),
    path('admin/', admin.site.urls),
    path('404/', handle_404),
    path('403/', handle_403),
    path('500/', handle_500),
    path('dashboard/', include([
        path('overview/', include('Dashboard.urls')),
        # path('organizers/', include('Organizers.urls')),
        path('associations/', include('Associations.urls')),
        path('events/', include('Events.urls')),
        path('users/', include('authentication.urls')),
        path('settings/', include([
            # TODO: Need to improve
            path('profile/', include([
                path('', settings_profile, name='settings'),
            ])),
        ])),
    ])),
    # TODO: need to improve,
    path('login/', signin, name='login'),
    path('register/', register, name='register'),
    path('account/request/verify/', request_verify_account, name='request-verify-account'),
    path('account/verify/<uidb64>/<token>/', verify_account, name='verify-account'),
    path('logout/', signout, name='logout')
]

# handler403 = handle_403
# handler404 = handle_404
# handler500 = handle_500

# media
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
