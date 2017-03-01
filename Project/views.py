from User.models import User
from generic.controller import PageNumberView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.detail import DetailView
from Project.models import Project
from django.views.generic.list import ListView
from django.db.models import Q
from django.views.generic.base import TemplateView
from Project.forms import ProjectCreateForm
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.views.generic.edit import DeleteView



class ProjectListView(PageNumberView, TemplateView):
    template_name = 'project/project_index.html'
    projects = None
    project = None
    paginator = None

    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            self.paginator = Paginator(Project.objects.all(), 10)
        else:
            self.paginator = Paginator(Project.objects.filter(Q(users=request.user)), 10)
        try:
            self.projects = self.paginator.page(request.GET['page'])
        except KeyError:
            self.projects = self.paginator.page(1)
        except EmptyPage:
            raise Http404()
        return super(ProjectListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context["projects"] = self.projects
        context['paginator'] = self.paginator
        return context


class ProjectCreate(TemplateView):
    model = Project
    template_name = 'project/add_project.html'
    form = None
    manager = None
    developer = None

    def get(self, request, *args, **kwargs):
        if request.user.role == "Manager" or request.user.is_admin:
            self.manager = User.objects.filter(role='Manager')
            self.developer = User.objects.filter(role='Developer')
            return super(ProjectCreate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('main'))

    def get_context_data(self, **kwargs):
        context = super(ProjectCreate, self).get_context_data(**kwargs)
        context['managers'] = self.manager
        context['developers'] = self.developer
        return context

    def post(self, request, *args, **kwargs):
        self.form = ProjectCreateForm(request.POST)
        if self.form.is_valid():
            if datetime.strptime(request.POST['due_date'], '%Y-%m-%d') <= datetime.today():
                messages.add_message(request,messages.ERROR,'Введенная дата неверна')
                return redirect(reverse('project_add'))
            else:
                self.form.save()
                return redirect(reverse('main'))
        else:
            messages.add_message(request, messages.ERROR, self.form.errors)
            return redirect(reverse('project_add'))


class ProjectUpdate(TemplateView):
    project = None
    template_name = 'project/project_edit.html'
    form = None
    manager = None
    developer = None
    user = None

    def get(self, request, *args, **kwargs):
        self.project = Project.objects.get(pk = self.kwargs['pk'])
        self.user = Project.objects.filter(users=request.user)
        if (request.user.role == "Manager" and self.user) or request.user.is_admin :
            self.form = ProjectCreateForm(instance=self.project)
            self.manager = User.objects.filter(role='Manager')
            self.developer = User.objects.filter(role='Developer')
            return super(ProjectUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('main'))

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['managers'] = self.manager
        context['developers'] = self.developer
        return context

    def post(self, request, *args, **kwargs):
        self.project = Project.objects.get(pk=self.kwargs['pk'])
        self.user = Project.objects.filter(users=request.user)
        if (request.user.role == "Manager" and self.user) or request.user.is_admin:
            self.form = ProjectCreateForm(request.POST,instance=self.project)
            if self.form.is_valid():
                self.form.save()
                return redirect(reverse('main'))
            else:
                return super(ProjectUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('main'))


class ProjectDelete(DeleteView):
    model = Project
    template_name = 'project/project_delete.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.project = Project.objects.get(pk=self.kwargs['pk'])
        self.user = Project.objects.filter(users=request.user)
        if (request.user.role == "Manager" and self.user) or request.user.is_admin:
            return super(ProjectDelete, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('main'))

    def post(self, request, *args, **kwargs):
        self.project = Project.objects.get(pk=self.kwargs['pk'])
        self.user = Project.objects.filter(users=request.user)
        if (request.user.role == "Manager" and self.user) or request.user.is_admin:
            self.success_url = reverse('main')
            return super(ProjectDelete, self).post(request, *args, **kwargs)
        else:
            return redirect(reverse('main'))