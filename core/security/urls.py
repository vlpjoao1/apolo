from django.urls import path

from core.security.views.access_user.views import *

urlpatterns = [
    path('list/', AccessUserListView.as_view(), name='access_user_list'),
]
