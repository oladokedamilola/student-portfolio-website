from django import forms
from accounts.models import *

class MatricVerificationForm(forms.Form):
    matric_number = forms.CharField(
        max_length=20,
        error_messages={
            'required': "Matric number is required.",
            'max_length': "Matric number cannot exceed 20 characters.",
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your matric number'
        })
    )


class StudentRegistrationForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': "Email is required.",
            'invalid': "Please enter a valid email address.",
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        error_messages={'required': "Password is required."},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'id_password'
        })
    )
    confirm_password = forms.CharField(
        error_messages={'required': "Please confirm your password."},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'id_confirm_password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': "Email is required.",
            'invalid': "Please enter a valid email address.",
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'id': 'id_email'
        })
    )
    password = forms.CharField(
        error_messages={'required': "Password is required."},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'id_password'
        })
    )


class ClientRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        error_messages={
            'required': "First name is required.",
            'max_length': "First name cannot exceed 50 characters.",
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        error_messages={
            'required': "Last name is required.",
            'max_length': "Last name cannot exceed 50 characters.",
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        error_messages={
            'required': "Email is required.",
            'invalid': "Please enter a valid email address.",
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    company_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company name (optional)'
        })
    )
    industry = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Industry (optional)'
        })
    )
    password = forms.CharField(
        error_messages={'required': "Password is required."},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'id_password'
        })
    )
    confirm_password = forms.CharField(
        error_messages={'required': "Please confirm your password."},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'id_confirm_password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['header', 'about', 'github_url', 'linkedin_url', 'profile_image']
        widgets = {
            'header': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Aspiring Data Scientist | Python & ML'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself',
                'rows': 3,
                'style': 'resize: none;'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'GitHub profile URL'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn profile URL'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class NINVerificationForm(forms.Form):
    nin = forms.CharField(
        max_length=11,
        error_messages={
            'required': "NIN is required.",
            'max_length': "NIN must not exceed 11 digits.",
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your NIN',
            'autocomplete': 'off'
        })
    )


class ClientProfileEditForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['first_name', 'last_name', 'company_name', 'industry', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter industry'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
