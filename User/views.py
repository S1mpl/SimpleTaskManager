from django.views.generic.base import TemplateView
from User.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

class RegisterUser(TemplateView):
    template_name = 'registration/register.html'
    form = None
    def post(self, request, *args, **kwargs):
        self.form = UserCreationForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            messages.add_message(request, messages.SUCCESS, 'Пользователь успешно зарегестрирован')
            return redirect(reverse('login'))
        else:
            messages.add_message(request, messages.ERROR,  self.form.errors)
            return redirect(reverse('register'))

