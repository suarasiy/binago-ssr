from django.urls import path

from .views import (
    index, index_approval, approval_accept, approval_reject
)

urlpatterns = [
    path('', index, name='associations'),
    path('approval/', index_approval, name='associations-approval'),
    path('approval/accept/<int:id>/', approval_accept, name='associations-approval-accept'),
    path('approval/reject/<int:id>/', approval_reject, name='associations-approval-reject'),
]
