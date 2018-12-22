from django.forms import ModelForm
from device.models import DeviceType, CustomField


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'tag': 'Tag',
            'desc': 'Description',
        }
        fields = ['tag', 'desc']


class CustomFieldForm(ModelForm):
    class Meta:
        model = CustomField
        labels = {
            'name': 'Name',
        }
        fields = ['name']
