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
from django.http import HttpResponse



class ProjectListView(PageNumberView, ListView):
    model = Project
    template_name = 'project/project_index.html'
    paginate_by = 10
    users = None

    def get(self, request, *args, **kwargs):
        self.users = Project.objects.filter(Q(users=request.user))
        return super(ProjectListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context["users"] = self.users
        return context


class ProjectCreate(TemplateView):
    model = Project
    template_name = 'project/add_project.html'
    form = None
    manager = None
    developer = None
    select_managers = []

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