from django.conf.urls import url
from django.contrib.auth.decorators import  login_required
from Task.views import TaskListView, TaskCreate, TaskUpdate, TaskDelete, TaskDetail, TaskEnd, TaskRestart

urlpatterns = [
    url(r'^$',  login_required(TaskListView.as_view()), name='task_main'),
    url(r'^task/(?P<pk>\d+)$', login_required(TaskDetail.as_view()), name='task_detail'),
    url(r'^task/add/$', login_required(TaskCreate.as_view()), name='task_add'),
    url(r'^task/(?P<pk>\d+)/edit/$', login_required(TaskUpdate.as_view()), name='task_edit'),
    url(r'^task/(?P<pk>\d+)/delete/$', login_required(TaskDelete.as_view()), name='task_delete'),
    url(r'^task/(?P<pk>\d+)/end/$', login_required(TaskEnd.as_view()), name='task_end'),
    url(r'^task/(?P<pk>\d+)/restart/$', login_required(TaskRestart.as_view()), name='task_restart'),
]