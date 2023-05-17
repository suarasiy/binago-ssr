from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler404, handler403, handler500
from django.conf.urls.static import static
from django.conf import settings

from . import views

from authentication.views import signin, register, verify_account, request_verify_account

if TYPE_CHECKING:
    from typing import Any


urlpatterns = [
    path('__reload__/', include('django_browser_reload.urls')),
    path('', views.index, name='homepage'),
    path('timeline/', views.timeline, name='homepage-timeline'),
    path('event/', include([
        path('', views.index, name='homepage-event'),
        path('<slug>/', include([
            path('', views.event_detail, name='homepage-event-detail'),
            path('register/', views.event_register, name='homepage-event-register'),
        ])),
    ])),
    path('upcoming/', include([
        path('', views.homepage, name='homepage-event-upcoming'),
        path('<category>/', views.homepage_category, name='homepage-event-upcoming-category'),
    ])),
    path('today/', include([
        path('', views.homepage_today, name='homepage-event-today'),
        path('<category>/', views.homepage_today_category, name='homepage-event-today-category'),
    ])),
    path('past/', include([
        path('', views.homepage_past, name='homepage-event-past'),
        path('<category>/', views.homepage_past_category, name='homepage-event-past-category'),
    ])),
    path('certificate/<str:uuid>/', views.index_certificate, name='homepage-certificate'),
    path('admin/', admin.site.urls),
    path('404/', views.handle_404),
    path('403/', views.handle_403),
    path('500/', views.handle_500),
    path('dashboard/', include([
        path('overview/', include('Dashboard.urls')),
        # path('organizers/', include('Organizers.urls')),
        path('associations/', include('Associations.urls')),
        path('events/', include('Events.urls')),
        path('users/', include('authentication.urls')),
        path('invoices/', include('Invoices.urls')),
        path('settings/', include([
            # TODO: Need to improve
            path('profile/', include([
                # TODO: Change it later
                path('', views.settings_profile, name='settings'),
            ])),
        ])),
    ])),
    # TODO: need to improve,
    path('login/', signin, name='login'),
    path('register/', register, name='register'),
    path('account/request/verify/', request_verify_account, name='request-verify-account'),
    path('account/verify/<uidb64>/<token>/', verify_account, name='verify-account'),
    path('logout/', views.signout, name='logout'),
    # apis handle
    path('api/', include([
        path('v1/', include([
            path('invoices/', include('Invoices.urls_api'))
        ]))
    ]))
]

# handler403 = handle_403
# handler404 = handle_404
# handler500 = handle_500

# media
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
