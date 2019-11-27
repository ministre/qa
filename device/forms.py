from django.forms import ModelForm, HiddenInput
from device.models import DeviceType, Vendor, CustomField, Device, DevicePhoto, Button, Led, Interface
from django.utils.translation import gettext_lazy as _


class InterfaceForm(ModelForm):
    class Meta:
        model = Interface
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'


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
            'desc_genitive': _('Genitive Description'),
            'cf': _('Custom fields'),
            'ifaces': _('Interfaces'),
            'redmine_url': _('Redmine URL'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        labels = {
            'vendor': _('Vendor'),
            'model': _('Model'),
            'hw': _('Hardware'),
            'type': _('Type'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


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
