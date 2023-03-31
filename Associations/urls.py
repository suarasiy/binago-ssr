from django.urls import path

from .views import (
    index, index_approval
)

urlpatterns = [
    path('', index, name='associations'),
    path('approval/', index_approval, name='associations-approval')
]
