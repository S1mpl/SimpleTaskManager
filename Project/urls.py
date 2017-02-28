from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.decorators import  permission_required

urlpatterns = [
    url(r'^$',  views.login, name='main'),
]