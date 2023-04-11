from django.urls import path, include

from .views import (
    index, index_data, edit, signin, register, profile, enable_disable_account,
)

urlpatterns = [
    path('', index, name='users'),
    # path('login/', signin, name='login'),
    # path('register/', register, name='register'),
    path('data/', include([
        path('', index_data, name='users-data'),
        path('profile/<str:username>/', profile, name='users-profile'),
        path('e_d/<int:id>/', enable_disable_account, name='users-enable-disable'),
    ])),
    path('settings/', include([
        path('profile/', include([
            path('edit/', edit, name='settings-edit'),
        ]))
    ])),
    path('notification/', include('NotificationHandler.urls'))
]
