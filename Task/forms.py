from Task.models import Task
from django import forms

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date','create_manager', 'project', 'developer']