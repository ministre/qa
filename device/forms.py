from django.forms import ModelForm, HiddenInput
from device.models import DeviceType, Vendor, CustomField, CustomFieldItem, Device, DevicePhoto, Sample
from django.utils.translation import gettext_lazy as _
from django import forms


class CustomFieldForm(ModelForm):
    class Meta:
        model = CustomField
        labels = {
            'name': _('Name'),
            'desc': _('Description'),
            'type': _('Value Type'),
        }
        fields = '__all__'
        TYPE = (
            ('text', 'Text'),
            ('number', 'Number'),
            ('listbox', 'Listbox'),
            ('checkbox', 'Checkbox'),
        )
        widgets = {
            'type': forms.Select(choices=TYPE, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class CustomFieldItemForm(ModelForm):
    class Meta:
        model = CustomFieldItem
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {
            'custom_field': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'tag': _('Tag'),
            'desc': _('Description'),
            'desc_genitive': _('Genitive Description'),
            'cf': _('Custom fields'),
            'redmine_project': _('Redmine Project ID'),
            'redmine_project_name': _('Redmine Project Name'),
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
            'type': _('Type'),
            'vendor': _('Vendor'),
            'model': _('Model'),
            'hw': _('Hardware'),
            'redmine_project': _('Redmine Project ID'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DevicePhotoForm(ModelForm):
    class Meta:
        model = DevicePhoto
        labels = {
            'photo': _('Photo'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        labels = {
            'sn': _('Serial Number'),
            'desc': _('Description'),
            'user_login': _('User Login'),
            'user_password': _('User Password'),
            'support_login': _('Support Login'),
            'support_password': _('Support Password'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
