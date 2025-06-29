from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'repo_link', 'project_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your project'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Technologies used'}),
            'repo_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Repository link (if any)'}),
            'project_file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx', 'class': 'form-control'}),
        }


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['title', 'abstract', 'publication_link', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Research title'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Brief abstract'}),
            'publication_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Publication link'}),
            'document': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx', 'class': 'form-control'}),
            
        }


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['organization', 'role', 'duration', 'summary']
        widgets = {
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role or position'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3 months'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What did you learn?'}),
        }



