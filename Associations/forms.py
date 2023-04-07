from django import forms
from .models import Associations, AssociationsGroup


class AssociationForm(forms.ModelForm):
    name = forms.CharField(max_length=80, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your association name...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'name'
        }
    ))
    location = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your association location based...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'location'
        }
    ))
    about = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'input__field min__h__50px',
            'placeholder': 'Describe abour your association...',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'rows': '8',
            'id': 'about'
        }
    ))
    email = forms.EmailField(min_length=8, max_length=80, widget=forms.EmailInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Your association email',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'email'
        }
    ))
    phone = forms.CharField(min_length=3, max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Association contact number',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'phone'
        }
    ))
    logo = forms.ImageField(
        allow_empty_file=False, required=True, widget=forms.ClearableFileInput(
            attrs={
                'class': 'input__field__file',
                'accept': 'image/*',
                'id': 'logo'
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
    website = forms.URLField(max_length=80, widget=forms.TextInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Association Website URL (optional)',
            'spellcheck': 'false',
            'autocomplete': 'off',
            'id': 'website'
        }
    )
    )

    class Meta:
        model = Associations
        fields = [
            'name', 'location', 'about', 'email', 'phone', 'logo', 'banner', 'website'
        ]


class AssociationInviteForm(forms.Form):
    email = forms.EmailField(min_length=8, max_length=80, widget=forms.EmailInput(
        attrs={
            'class': 'input__field',
            'placeholder': 'Input user\'s email to send invitation',
            'spellcheck': 'false',
            'id': 'email',
            'autocomplete': 'off'
        }
    ))
