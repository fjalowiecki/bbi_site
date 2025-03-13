from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 
            'short_description', 
            'description', 
            'people_involved_nb', 
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
            'tags'
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }