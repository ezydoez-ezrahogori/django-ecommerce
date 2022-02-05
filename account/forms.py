from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'autofocus': 'autofocus'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter old password'
            }
        ))
    new_password1 = forms.CharField(
        max_length=100, widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter new password'
            }
        ))
    new_password2 = forms.CharField(
        max_length=100, widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm new password'
            }
        ))
