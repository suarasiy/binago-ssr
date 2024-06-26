from django.urls import path, include

from Events import views as events

from .views import (
    index, index_data, index_data_approval, approval_accept, approval_reject, profile, invite,
    edit_profile, explore, create, event_preview_resources, event_new_stream, event_stream_destroy
)

urlpatterns = [
    path('', index, name='associations'),
    path('data/', include([
        path('', index_data, name='associations-data'),
        path('create/', create, name='associations-create'),
        path('approval/', index_data_approval, name='associations-data-approval'),
        path('approval/accept/<int:id>/', approval_accept, name='associations-data-approval-accept'),
        path('approval/reject/<int:id>/', approval_reject, name='associations-data-approval-reject'),
        path('<slug:slug>/', include([
            path('', explore, name='associations-data-explore'),
            path('invite/', invite, name='associations-data-invite'),
            path('events/', include([
                path('', events.association_events, name='events-association'),
                path('create/', events.events_create, name='events-create'),
                path('streamlink/<slug_event>/', event_new_stream, name='events-new-stream'),
                path('streamlink/<slug_event>/destroy/<id_stream>/', event_stream_destroy, name='events-destroy-stream'),
                path('preview/<slug_event>/', event_preview_resources, name='associations-event-preview'),
                path('edit/<slug_event>/', events.events_edit, name='events-edit'),
                path('destroy/<slug_event>/', events.events_destroy, name='events-destroy')
            ]))
        ])),
    ])),
    path('profile/<slug:slug>/', include([
        path('', profile, name='associations-profile'),
        path('edit/', edit_profile, name='associations-edit'),
    ]))
]
