from django.urls import path, include

from Events import views as events

from .views import (
    index, index_data, index_data_approval, approval_accept, approval_reject, profile, invite,
    edit_profile, explore
)

urlpatterns = [
    path('', index, name='associations'),
    path('data/', include([
        path('', index_data, name='associations-data'),
        path('approval/', index_data_approval, name='associations-data-approval'),
        path('approval/accept/<int:id>/', approval_accept, name='associations-data-approval-accept'),
        path('approval/reject/<int:id>/', approval_reject, name='associations-data-approval-reject'),
        path('<slug:slug>/', include([
            path('', explore, name='associations-data-explore'),
            path('invite/', invite, name='associations-data-invite'),
            path('events/', include([
                path('', events.association_events, name='events-association'),
                path('create/', events.events_create, name='events-create'),
                path('edit/<slug_event>/', events.events_edit, name='events-edit'),
                path('destroy/<slug_event>/', events.events_destroy, name='events-destroy')
            ]))
        ]))
    ])),
    path('profile/<slug:slug>/', include([
        path('', profile, name='associations-profile'),
        path('edit/', edit_profile, name='associations-edit'),
    ]))
]
