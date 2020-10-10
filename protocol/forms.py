from django.forms import ModelForm, HiddenInput
from .models import Branch, Protocol
from django.utils.translation import gettext_lazy as _


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
            'started': _('Date of start'),
            'completed': _('Date of completion'),
            'status': _('Status'),
            'scan': _('Scan-copy of protocol'),
        }
        fields = '__all__'
        widgets = {
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
