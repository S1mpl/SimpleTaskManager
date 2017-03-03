from django import forms
from Project.models import Project

class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title','due_date','users', 'description']

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False