from django.forms import ModelForm, HiddenInput
from .models import Firmware
from django.utils.translation import gettext_lazy as _


class FirmwareForm(ModelForm):
    class Meta:
        model = Firmware
        labels = {
            'device': _('Device'),
            'version': _('Version'),
            'file': _('File'),
            'checksum': _('Checksum'),
            'sysinfo_cli': _('CLI System Information'),
            'sysinfo_snapshot': _('WebUI System Information'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
