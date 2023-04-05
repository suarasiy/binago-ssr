from django.urls import path

from .views import (
    edit, signin, register
)

urlpatterns = [
    path('login/', signin, name='login'),
    path('register/', register, name='register'),
    path('edit/', edit, name='settings-edit'),
]
