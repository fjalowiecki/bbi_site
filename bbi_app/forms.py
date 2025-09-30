from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 
            'description', 
            'year_of_completion',
            'location',
            'financing_type',
            'financing_type_other',
            'proj_site',
            'contact_info',
            'image1',
            'image2',
            'image3',
            'image4',
            'main_image',
            'tags'
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }