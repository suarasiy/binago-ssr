from django.urls import path
from .views import (
    index, events_create, events_edit, events_destroy
)

urlpatterns = [
    # path('', index, name='events'),
    # path('create/', events_create, name='events-create'),
    # path('edit/<str:slug>/', events_edit, name='events-edit'),
    # path('destroy/<str:slug>/', events_destroy, name='events-destroy')
]
