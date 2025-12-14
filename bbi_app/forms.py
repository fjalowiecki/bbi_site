import io, os, pillow_heif
from django import forms
from .models import Project, ProjectLink, ProjectFile
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

# Zarejestruj obsługę HEIF w Pillow
pillow_heif.register_heif_opener()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 
            'organization_name',
            'description', 
            'year_of_completion',
            'location',
            'financing_type',
            'financing_type_other',
            'contact_info',
            'user_email',
            'image1',
            'image2',
            'image3',
            'image4',
            'tags'
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 6}),
            'contact_info': forms.Textarea(attrs={'rows': 3}),
        }
    
    def _validate_file_size(self, image_field):
        """Sprawdza czy rozmiar pliku nie przekracza 4MB"""
        if image_field and image_field.size > 4 * 1024 * 1024:  # 4MB w bajtach
            raise forms.ValidationError('Rozmiar pliku nie może przekraczać 4MB.')
        return image_field
    
    def _convert_to_jpg(self, image_field):
        """Konwertuje HEIC do JPG"""
        if not image_field:
            return image_field
            
        # Sprawdź czy to plik wymagający konwersji
        if image_field.name.lower().endswith(('.heic', '.heif')):
            # Otwórz obraz
            img = Image.open(image_field)
            
            # Konwertuj do RGB jeśli potrzeba
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Zapisz jako JPEG
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)
            
            # Stwórz nowy plik
            new_name = image_field.name.rsplit('.', 1)[0] + '.jpg'
            return InMemoryUploadedFile(
                output, 
                'ImageField', 
                new_name, 
                'image/jpeg',
                output.getbuffer().nbytes, 
                None
            )
        
        return image_field
    
    def clean_image1(self):
        image = self.cleaned_data.get('image1')
        self._validate_file_size(image)
        return self._convert_to_jpg(image)
    
    def clean_image2(self):
        image = self.cleaned_data.get('image2')
        self._validate_file_size(image)
        return self._convert_to_jpg(image)
    
    def clean_image3(self):
        image = self.cleaned_data.get('image3')
        self._validate_file_size(image)
        return self._convert_to_jpg(image)
    
    def clean_image4(self):
        image = self.cleaned_data.get('image4')
        self._validate_file_size(image)
        return self._convert_to_jpg(image)
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 40:
            raise forms.ValidationError('Tytuł nie może być dłuższy niż 40 znaków.')
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 500:
            raise forms.ValidationError('Opis nie może być dłuższy niż 500 znaków.')
        return description
    
    def clean_contact_info(self):
        contact_info = self.cleaned_data.get('contact_info')
        if contact_info and len(contact_info) > 100:
            raise forms.ValidationError('Dane kontaktowe nie mogą być dłuższe niż 100 znaków.')
        return contact_info
        
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

class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ('name', 'file')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Walidacja rozmiaru
            if file.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('Rozmiar pliku nie może przekraczać 10MB.')

            # Walidacja typu pliku
            ext = os.path.splitext(file.name)[1]  # Pobierz rozszerzenie pliku
            valid_extensions = [
                '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',  # Tekstowe
                '.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.webp', '.heic', # Graficzne
                '.mp4', '.mov', '.avi', '.wmv', '.mkv', '.webm' # Wideo
            ]
            if not ext.lower() in valid_extensions:
                raise forms.ValidationError('Niedozwolony typ pliku. Akceptowane są pliki tekstowe (np. PDF, DOCX), graficzne (np. JPG, PNG) oraz wideo (np. MP4, MOV).')
                
        return file

ProjectFileFormSet = forms.inlineformset_factory(
    Project,
    ProjectFile,
    form=ProjectFileForm,
    fields=('name', 'file'),
    extra=1,
    can_delete=False
)