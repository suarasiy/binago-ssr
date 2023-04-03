from django import forms
from django.db import models

from .models import User


class Gender(models.TextChoices):
    MALE = "M", ("Male")
    FEMALE = "F", ("Female")
    HIDE = "H", ("Hide Gender")


class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=100, min_length=5, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your username...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'username',
        }
    ))
    first_name = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your first name...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'first_name',
        }
    ))
    last_name = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your last name...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'last_name',
        }
    ))
    email = forms.CharField(max_length=80, min_length=8, widget=forms.EmailInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your email...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'email',
        }
    ))
    about = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'class': 'input__field min__h__50px',
            'placeholder': 'Describe about yourself...',
            'spellcheck': 'false',
            'rows': '8',
            'autocomplete': 'off',
            'id': 'about',
        }
    ))
    avatar = forms.ImageField(
        allow_empty_file=False, required=True, widget=forms.ClearableFileInput(
            attrs={
                'class': 'input__field__file',
                'accept': 'image/*',
                'id': 'avatar'
            }
        )
    )
    banner = forms.ImageField(
        allow_empty_file=False, required=True, widget=forms.ClearableFileInput(
            attrs={
                'class': 'input__field__file',
                'accept': 'image/*',
                'id': 'banner'
            }
        )
    )
    institute = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your institution...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'institute',
        }
    ))
    gender = forms.ChoiceField(choices=Gender.choices, widget=forms.RadioSelect(
        attrs={
            'class': 'input__field',
            'id': 'gender'
        }
    ))
    city = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your city...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'city'
        }
    ))

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'city',
            'about', 'avatar', 'banner', 'gender', 'institute',
        ]
