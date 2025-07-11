from django import forms
from .models import Project, Research, Internship, Skill

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'repo_link', 'project_file']  # Removed 'skills'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your project', 'rows': 4, 'style': 'resize: none;'}),
            'technologies': forms.TextInput(attrs={'placeholder': 'Technologies used'}),
            'repo_link': forms.URLInput(attrs={'placeholder': 'Repository link (if any)'}),
            'project_file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['title', 'abstract', 'publication_link', 'document'] 
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Research title'}),
            'abstract': forms.Textarea(attrs={'placeholder': 'Brief abstract', 'rows': 4, 'style': 'resize: none;'}),
            'publication_link': forms.URLInput(attrs={'placeholder': 'Publication link'}),
            'document': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['organization', 'role', 'duration', 'summary']
        widgets = {
            'organization': forms.TextInput(attrs={'placeholder': 'Organization name'}),
            'role': forms.TextInput(attrs={'placeholder': 'Role or position'}),
            'duration': forms.TextInput(attrs={'placeholder': 'e.g., 3 months'}),
            'summary': forms.Textarea(attrs={'placeholder': 'What did you learn?', 'rows': 4, 'style': 'resize: none;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'

