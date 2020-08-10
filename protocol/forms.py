from django.forms import ModelForm, HiddenInput
from .models import Protocol
from django.utils.translation import gettext_lazy as _


class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        labels = {
            'device': _('Device'),
            'testplan': _('Testplan'),
            #'firmware': _('Firmware'),
            'started': _('Date of start'),
            'completed': _('Date of completion'),
            'status': _('Status'),
            'sample': _('Sample'),
            'scan': _('Scan-copy of protocol'),
        }
        fields = '__all__'
        widgets = {
            'device': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
