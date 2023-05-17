from django.urls import path
from . import views

urlpatterns = [
    path('update-status/', views.update_payment_status, name='api-invoice-update-status')
]
