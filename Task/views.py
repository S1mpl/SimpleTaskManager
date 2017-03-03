from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.detail import DetailView
from Project.models import Project
from django.views.generic.base import TemplateView
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.views.generic.edit import DeleteView
from Task.models import Task, TaskFiles
from django.forms.models import inlineformset_factory
from Task.forms import TaskCreateForm

TaskFilesFormset = inlineformset_factory(Task, TaskFiles, fields=['files'], can_delete=False,  extra=1, max_num=10)

class TaskListView(TemplateView):
    template_name = 'task/task_index.html'
    user = None
    paginator = None
    tasks = None
    request = None
    project = None

    def get(self, request, *args, **kwargs):
        self.request = request
        self.user = Project.objects.filter(pk=self.kwargs['pk_project'], users=request.user.id)
        if request.user.is_admin or self.user:
            if request.user.role == 'Developer':
                self.paginator = Paginator(Task.objects.filter(project=self.kwargs['pk_project'], developer=request.user), 10)
            else:
                self.paginator = Paginator(Task.objects.filter(project=self.kwargs['pk_project']), 10)
        else:
            return redirect(reverse('main'))
        try:
            self.tasks = self.paginator.page(request.GET['page'])
        except KeyError:
            self.tasks = self.paginator.page(1)
        except EmptyPage:
            raise Http404()
        return super(TaskListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["tasks"] = self.tasks
        context['paginator'] = self.paginator
        context['project_id'] = self.kwargs['pk_project']
        return context

class TaskCreate(TemplateView):
    template_name = 'task/task_create.html'
    form = None
    formset = None
    developers = None

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_admin:
                self.user = Project.objects.get(pk=self.kwargs['pk_project'])
            else:
                self.user = Project.objects.get(pk=self.kwargs['pk_project'], users=request.user.id)
        except:
            raise Http404()
        if request.user.is_admin or (self.user and request.user.role == 'Manager'):
            self.formset = TaskFilesFormset()
            self.developers = Project.objects.filter(pk=self.kwargs['pk_project'], users__role='Developer').values('users','users__firstname','users__lastname', 'users__email')
            return super(TaskCreate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('main'))


    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['formset'] = self.formset
        context['developers'] = self.developers
        return context

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['due_date'] = request.POST['due_date'].replace('T',' ')
        request.POST['create_manager'] = request.user.id
        request.POST['project'] = self.kwargs['pk_project']
        self.form = TaskCreateForm(request.POST, request.FILES)
        if self.form.is_valid():
            if datetime.strptime(request.POST['due_date'], '%Y-%m-%d %H:%M') <= datetime.now():
                messages.add_message(request,messages.ERROR,'Введенная дата неверна')
                return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))
            new_task = self.form.save()
            self.formset = TaskFilesFormset(request.POST, request.FILES, instance=new_task)
            if self.formset.is_valid():
                self.formset.save()
                return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))
            else:
                messages.add_message(request, messages.ERROR, self.formset.errors)
                return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))
        else:
            messages.add_message(request, messages.ERROR, self.form.errors)
            return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))

class TaskUpdate(TemplateView):
    template_name = 'task/task_update.html'
    task = None
    form =None
    formset = None
    user = None
    task_dev = None

    def get(self, request, *args, **kwargs):
        try:
            self.user = Project.objects.filter(pk=self.kwargs['pk_project'], users=request.user)
        except:
            raise Http404()
        if request.user.is_admin or (self.user and request.user.role == 'Manager'):
            self.task = Task.objects.get(pk=self.kwargs['pk'])
            self.form = TaskCreateForm(instance=self.task)
            self.formset = TaskFilesFormset(instance=self.task)
            self.task_dev = Task.objects.filter(pk=self.kwargs['pk']).values('developer')
            self.developers = Project.objects.filter(pk=self.kwargs['pk_project'], users__role='Developer').values('users','users__firstname','users__lastname', 'users__email')
        else:
            return redirect(reverse('main'))
        return super(TaskUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['task'] = self.task
        context['form'] = self.form
        context['formset'] = self.formset
        context['developers'] = self.developers
        context['task_dev'] = self.task_dev
        return context

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['due_date'] = request.POST['due_date'].replace('T', ' ')
        request.POST['create_manager'] = request.user.id
        request.POST['project'] = self.kwargs['pk_project']
        self.task = Task.objects.get(pk=self.kwargs['pk'])
        self.form = TaskCreateForm(request.POST, request.FILES, instance=self.task)
        if self.form.is_valid():
            if datetime.strptime(request.POST['due_date'], '%Y-%m-%d %H:%M') <= datetime.now():
                messages.add_message(request, messages.ERROR, 'Введенная дата неверна')
                return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))
            new_task = self.form.save()
            self.formset = TaskFilesFormset(request.POST, request.FILES, instance=new_task)
            if self.formset.is_valid():
                self.formset.save()
                return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))
            else:
                messages.add_message(request, messages.ERROR, self.formset.errors)
                return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))
        else:
            messages.add_message(request, messages.ERROR, self.form.errors)
            return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))


class TaskDelete(DeleteView):
    model = Task
    template_name = 'task/task_delete.html'

    user = None

    def get(self, request, *args, **kwargs):
        self.user = Project.objects.filter(users=request.user, pk=self.kwargs['pk_project'])
        if (request.user.role == "Manager" and self.user) or request.user.is_admin:
            return super(TaskDelete, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk_project']
        self.success_url = reverse('task_main', kwargs={'pk_project':pk})
        return super(TaskDelete, self).post(request, *args, **kwargs)

class TaskDetail(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    developer = None
    manager = None

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == "Developer":
                self.developer = Task.objects.get(developer=request.user, pk=self.kwargs['pk'])
            self.manager = Project.objects.filter(users=request.user, pk=self.kwargs['pk_project'])
        except:
            raise Http404
        if  self.manager or self.developer or request.user.is_admin:
            return super(TaskDetail, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context['files'] = TaskFiles.objects.filter(task=self.kwargs['pk'])
        context['pk_project'] = self.kwargs['pk_project']
        return context

class TaskEnd(TemplateView):
    template_name = 'task/task_end.html'
    developer = None
    manager = None
    task = None

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == "Developer":
                self.developer = Task.objects.get(developer=request.user, pk=self.kwargs['pk'])
            self.manager = Project.objects.filter(users=request.user, pk=self.kwargs['pk_project'])
        except:
            raise Http404
        if  self.manager or self.developer or request.user.is_admin:
            return super(TaskEnd, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))

    def post(self, request, *args, **kwargs):
        self.task = Task.objects.get(pk=self.kwargs['pk'])
        self.task.is_active = 0
        self.task.save()
        return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))

class TaskRestart(TemplateView):
        template_name = 'task/task_restart.html'
        developer = None
        manager = None
        task = None

        def get(self, request, *args, **kwargs):
            try:
                if request.user.role == "Developer":
                    raise Http404
                self.manager = Project.objects.filter(users=request.user, pk=self.kwargs['pk_project'])
            except:
                raise Http404
            if self.manager or request.user.is_admin:
                return super(TaskRestart, self).get(request, *args, **kwargs)
            else:
                return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))

        def post(self, request, *args, **kwargs):
            self.task = Task.objects.get(pk=self.kwargs['pk'])
            self.task.is_active = 1
            self.task.save()
            return redirect(reverse("task_main", kwargs={"pk_project": self.kwargs['pk_project']}))