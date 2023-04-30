from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='events'),
    path('registered/', include([
        path('',  views.index_registered, name='events-registered'),
        path('<int:ticket_id>/', views.event_resources, name='events-registered-resources')
    ])),
    # path('create/', events_create, name='events-create'),
    # path('edit/<str:slug>/', events_edit, name='events-edit'),
    # path('destroy/<str:slug>/', events_destroy, name='events-destroy')
]
