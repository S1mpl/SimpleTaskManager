from django.views.generic.base import TemplateView
from User.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from User.models import User
from django.core.paginator import Paginator, EmptyPage
from django.views.generic.edit import DeleteView

class RegisterUser(TemplateView):
    template_name = 'registration/register.html'
    form = None
    def post(self, request, *args, **kwargs):
        self.form = UserCreationForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            messages.add_message(request, messages.SUCCESS, 'Пользователь успешно зарегестрирован')
            if request.user.is_authenticated:
                return redirect(reverse('users'))
            else:
                return redirect(reverse('login'))
        else:
            messages.add_message(request, messages.ERROR,  self.form.errors)
            return redirect(reverse('register'))

class UserList(TemplateView):
    template_name = 'registration/user_list.html'
    users = None
    paginator = None

    def get(self, request, *args, **kwargs):
        if request.user.role == 'Manager':
            self.paginator = Paginator(User.objects.filter(role='Developer'), 10)
        elif request.user.is_admin:
            self.paginator = Paginator(User.objects.all(), 10)
        else:
            raise Http404
        try:
            self.users = self.paginator.page(request.GET['page'])
        except KeyError:
            self.users = self.paginator.page(1)
        except EmptyPage:
            raise Http404()
        return super(UserList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context["users"] = self.users
        context['paginator'] = self.paginator
        context['current_url'] = self.request.path
        return context

class UserDelete(TemplateView):
    template_name = 'registration/user_delete.html'

    usere = None

    def get(self, request, *args, **kwargs):
        self.usere = User.objects.get(pk=self.kwargs['pk'])
        if request.user.role == "Manager"  or request.user.is_admin:
            if request.user.role == 'Manager' and self.usere.role != 'Developer':
                raise Http404
            return super(UserDelete, self).get(request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        User.objects.get(pk=self.kwargs['pk']).delete()
        return redirect(reverse('users'))

class UserUpdate(TemplateView):
    template_name = 'registration/user_edit.html'
    form = None
    edit_user = None

    def get(self, request, *args, **kwargs):
        if request.user.role == 'Manager' or request.user.is_admin:
            self.edit_user = User.objects.get(pk=self.kwargs['pk'])
            if request.user.role == 'Manager' and self.edit_user.role != 'Developer':
                raise Http404
            self.form = UserChangeForm(instance=self.edit_user)
            return super(UserUpdate, self).get(request, *args, **kwargs)
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.edit_user = User.objects.get(pk=self.kwargs['pk'])
        self.form = UserChangeForm(request.POST, instance=self.edit_user)
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('users'))
        else:
            messages.add_message(request, messages.ERROR, self.form.errors)
            return super(UserUpdate, self).get(request, *args, **kwargs)