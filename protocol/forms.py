from django.forms import ModelForm, HiddenInput
from .models import Branch, Protocol
from django.utils.translation import gettext_lazy as _
from django import forms


class BranchForm(ModelForm):
    class Meta:
        model = Branch
        labels = {
            'name': _('Branch'),
        }
        fields = '__all__'
        widgets = {
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        labels = {
            'testplan': _('Testplan'),
            'started': _('Start Date'),
            'completed': _('Completion Date'),
            'status': _('Status'),
        }
        fields = '__all__'
        STATUS = (
            ('0', 'In progress'),
            ('1', 'Not recommended'),
            ('2', 'Recommended with limitation'),
            ('3', 'Recommended'),
        )
        widgets = {
            'status': forms.Select(choices=STATUS, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
