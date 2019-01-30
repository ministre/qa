from django.forms import ModelForm, HiddenInput
from device.models import DeviceType, CustomField, Device, DevicePhoto, Button, Led, Firmware
from django.utils.translation import gettext_lazy as _


class CustomFieldForm(ModelForm):
    class Meta:
        model = CustomField
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'tag': _('Tag'),
            'desc': _('Description'),
            'cf': _('Custom fields'),
        }
        fields = '__all__'


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        labels = {
            'vendor': _('Vendor'),
            'model': _('Model'),
            'hw': _('Hardware'),
            'type': _('Type'),
        }
        fields = ['vendor', 'model', 'hw', 'type', 'created_by']
        widgets = {'created_by': HiddenInput()}


class DevicePhotoForm(ModelForm):
    class Meta:
        model = DevicePhoto
        labels = {
            'device': _('Device'),
            'photo': _('Photo'),
            'desc': _('Description'),
        }
        fields = '__all__'


class ButtonForm(ModelForm):
    class Meta:
        model = Button
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'


class LedForm(ModelForm):
    class Meta:
        model = Led
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'


class FirmwareForm(ModelForm):
    class Meta:
        model = Firmware
        labels = {
            'device': _('Device'),
            'version': _('Version'),
            'file': _('File'),
            'desc': _('Description'),
        }
        fields = ['device', 'version', 'desc', 'file', 'created_by']
        widgets = {'created_by': HiddenInput()}
