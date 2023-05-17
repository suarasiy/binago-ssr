from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='invoices'),
    path('cancel/<int:id>/', views.cancel_invoices, name='invoices-cancel'),
    path('related/', include([
        path('a/<int:event_id>/', views.related_invoices, name='invoices-related'),
        path('p/<int:event_id>/', views.related_invoices_p, name='invoices-related-p'),
    ]))
]
