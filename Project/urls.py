from django.conf.urls import url, include
from django.contrib.auth import views
from django.contrib.auth.decorators import  login_required
from Project.views import ProjectListView, ProjectCreate, ProjectDelete, ProjectUpdate

urlpatterns = [
    url(r'^$',  login_required(ProjectListView.as_view()), name='main'),
    url(r'^project/(?P<pk_project>\d+)/', include('Task.urls'), name='project_task'),
    url(r'^project/add/$', login_required(ProjectCreate.as_view()), name='project_add'),
    url(r'^project/(?P<pk>\d+)/edit/$', login_required(ProjectUpdate.as_view()), name='project_edit'),
    url(r'^project/(?P<pk>\d+)/delete/$', login_required(ProjectDelete.as_view()), name='project_delete'),

    url(r'^project/(?P<pk>\d+)/end/$', login_required(ProjectDelete.as_view()), name='project_end'),
]