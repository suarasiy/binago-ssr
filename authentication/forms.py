from django import forms
from django.db import models
from django.core.exceptions import ValidationError

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


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=80, min_length=8, widget=forms.EmailInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Email',
            'autocomplete': 'off',
            'spellcheck': 'false',
            'id': 'email'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Password',
            'id': 'password'
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        email: str = cleaned_data.get('email', None)

        user: User | None = User.objects.filter(email=email).first()
        if user:
            if not user.is_verified:
                raise ValidationError("Please verify your account by activation link on your email in order to login.")

        return super().clean()


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'First name',
            'autocomplete': 'off',
            'spellcheck': 'false',
            'id': 'first_name'
        }
    ))
    last_name = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Last name',
            'autocomplete': 'off',
            'spellcheck': 'false',
            'id': 'last_name'
        }
    ))
    username = forms.CharField(max_length=100, min_length=5, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Username',
            'autocomplete': 'off',
            'spellcheck': 'false',
            'id': 'username'
        }
    ))
    email = forms.EmailField(max_length=80, min_length=8, widget=forms.EmailInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Email',
            'autocomplete': 'off',
            'spellcheck': 'false',
            'id': 'email'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Password',
            'id': 'password'
        }
    ))
    re_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Re-Type password',
            'id': 're_password'
        }
    ))

    def clean_re_password(self) -> str:
        password: str = self.cleaned_data.get('password', None)
        re_password: str = self.cleaned_data.get('re_password', None)

        if re_password != password:
            raise ValidationError("Re-type password is not matched.")

        return re_password

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get('password', None)
    #     re_password = cleaned_data.get('re_password', None)
    #     if password and re_password:
    #         if re_password != password:
    #             raise ValidationError("Re-type password is not matched.")
    #     return super().clean()

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password'
        ]
