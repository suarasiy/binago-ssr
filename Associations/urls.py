from django.urls import path, include

from .views import (
    index, index_data, index_data_approval, approval_accept, approval_reject, profile, invite,
    edit_profile
)

urlpatterns = [
    path('', index, name='associations'),
    path('data/', include([
        path('', index_data, name='associations-data'),
        path('approval/', index_data_approval, name='associations-data-approval'),
        path('approval/accept/<int:id>/', approval_accept, name='associations-data-approval-accept'),
        path('approval/reject/<int:id>/', approval_reject, name='associations-data-approval-reject'),
        path('invite/', invite, name='associations-data-invite'),
    ])),
    path('profile/', include([
        path('', profile, name='associations-profile'),
        path('edit/', edit_profile, name='associations-edit'),
    ]))
]
