from django import forms
from .models import Project, ProjectLink

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
        
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not tags or len(tags) == 0:
            raise forms.ValidationError('Proszę wybrać przynajmniej jeden tag.')
        if len(tags) > 5:
            raise forms.ValidationError('Możesz wybrać maksymalnie 5 tagów.')
        return tags

class ProjectLinkForm(forms.ModelForm):
    class Meta:
        model = ProjectLink
        fields = ('name', 'url')
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

ProjectLinkFormSet = forms.inlineformset_factory(
    Project,
    ProjectLink,
    form=ProjectLinkForm,
    fields=('name', 'url'),
    extra=1,
    can_delete=False
)