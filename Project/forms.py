from django import forms
from Project.models import Project

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description','due_date','users']