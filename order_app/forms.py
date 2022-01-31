from django import forms
from .models import Offer, ExtraTask



class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'label',
            'expenses',
            'Note',
            ]

class EditeOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'label',
            'expenses',
            'Note',
            ]


class ExtraTaskForm(forms.ModelForm):
    class Meta:
        model = ExtraTask
        fields = [
            'date',
            'time',
            'description',
            'lebal',
            'expenses',
            'upload_file_if_any',
            'extra_note',
            ]



class EditeExtraTaskForm(forms.ModelForm):
    class Meta:
        model = ExtraTask
        fields = [
            'date',
            'time',
            'description',
            'lebal',
            'expenses',
            'upload_file_if_any',
            'extra_note',
            ]
