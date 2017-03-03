from django.conf.urls import url
from django.contrib.auth.decorators import  login_required
from User.views import UserList, UserDelete, UserUpdate

urlpatterns = [
    url(r'^$',  login_required(UserList.as_view()), name='users'),
    url(r'^(?P<pk>\d+)/delete/$',  login_required(UserDelete.as_view()), name='delete_user'),
    url(r'^(?P<pk>\d+)/edit/$',  login_required(UserUpdate.as_view()), name='update_user'),
]