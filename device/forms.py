from django.forms import ModelForm
from device.models import DeviceType, CustomField


class CustomFieldForm(ModelForm):
    class Meta:
        model = CustomField
        labels = {
            'name': 'Name',
        }
        fields = ['name']


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'tag': 'Tag',
            'desc': 'Description',
            'cf': 'Custom fields',
        }
        fields = ['tag', 'desc', 'cf']
