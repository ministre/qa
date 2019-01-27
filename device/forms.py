from django.forms import ModelForm
from device.models import DeviceType, CustomField, Device, DevicePhoto, Button, Led, Firmware
from django.utils.translation import gettext_lazy as _


class CustomFieldForm(ModelForm):
    class Meta:
        model = CustomField
        labels = {
            'name': _('Name'),
        }
        fields = ['name']


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'tag': _('Tag'),
            'desc': _('Description'),
            'cf': _('Custom fields'),
        }
        fields = ['tag', 'desc', 'cf']


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        labels = {
            'vendor': _('Vendor'),
            'model': _('Model'),
            'hw': _('Hardware'),
            'type': _('Type'),
        }
        fields = ['vendor', 'model', 'hw', 'type']


class DevicePhotoForm(ModelForm):
    class Meta:
        model = DevicePhoto
        labels = {
            'device': _('Device'),
            'photo': _('Photo'),
            'desc': _('Description'),
        }
        fields = ['device', 'photo', 'desc']


class ButtonForm(ModelForm):
    class Meta:
        model = Button
        labels = {
            'name': _('Name'),
        }
        fields = ['name']


class LedForm(ModelForm):
    class Meta:
        model = Led
        labels = {
            'name': _('Name'),
        }
        fields = ['name']


class FirmwareForm(ModelForm):
    class Meta:
        model = Firmware
        labels = {
            'device': _('Device'),
            'version': _('Version'),
            'file': _('File'),
            'desc': _('Description'),
        }
        fields = ['device', 'version', 'file', 'desc']
