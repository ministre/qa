from django.forms import ModelForm, HiddenInput
from .models import Branch, Protocol, ProtocolDevice, ProtocolScan
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
            'started': _('Started'),
            'completed': _('Completed'),
            'status': _('Status'),
        }
        fields = '__all__'
        STATUS = (
            ('0', 'In progress'),
            ('1', 'Not recommended'),
            ('2', 'Partially recommended'),
            ('3', 'Recommended'),
        )
        widgets = {
            'status': forms.Select(choices=STATUS, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolDeviceForm(ModelForm):
    class Meta:
        model = ProtocolDevice
        labels = {
            'device': _('Device'),
            'firmware': _('Firmware'),
            'sample': _('Sample'),
        }
        fields = '__all__'
        widgets = {
            'protocol': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolScanForm(ModelForm):
    class Meta:
        model = ProtocolScan
        labels = {
            'scan': _('Scan'),
        }
        fields = '__all__'
        widgets = {
            'protocol': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
