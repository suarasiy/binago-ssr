from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='invoices'),
    path('cancel/<int:id>/', views.cancel_invoices, name='invoices-cancel'),
    path('<int:event_id>/', views.related_invoices, name='invoices-related'),
]
