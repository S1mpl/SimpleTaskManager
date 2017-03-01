from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.decorators import  login_required
from Project.views import ProjectListView, ProjectCreate

urlpatterns = [
    url(r'^$',  login_required(ProjectListView.as_view()), name='main'),
    url(r'^project/(?P<pk>\d+)$', login_required(views.login), name='project_task'),
    url(r'^project/add/$', login_required(ProjectCreate.as_view()), name='project_add'),
    url(r'^project/(?P<pk>\d+)/edit/$', login_required(views.login), name='project_edit'),
    url(r'^project/(?P<pk>\d+)/delete/$', login_required(views.login), name='project_delete'),
]