from django.urls import path
from .views import (
    index, events_create
)

urlpatterns = [
    path('', index, name='events'),
    path('create/', events_create, name='events-create')
]
