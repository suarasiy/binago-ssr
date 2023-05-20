from django.urls import path, include

from .views import events, payments


urlpatterns = [
    path('', include([
        path('', events, name='dashboard'),
        path('events/', events, name='dashboard-events'),
        path('payments/', payments, name='dashboard-payments')
    ])),
]
