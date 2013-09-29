from django import forms
from django_ace import AceWidget

from .models import Chord


class ChordAdminForm(forms.ModelForm):
    class Meta:
        model = Chord
        widgets = {
            'configuration': AceWidget(mode='json', theme='solarized_light', attrs={'style': 'width:1000px'})
        }
