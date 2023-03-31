from django import forms
from .models import Associations


class AssociationForm(forms.ModelForm):

    class Meta:
        model = Associations
        fields = ['user', 'name', 'slug', 'location', 'about',
                  'email', 'phone', 'logo', 'banner']
