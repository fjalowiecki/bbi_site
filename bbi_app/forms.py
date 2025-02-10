from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['short_title', 'full_title', 'description', 'start_date', 'end_date']
