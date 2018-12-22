from django.forms import ModelForm
from device.models import DeviceType, CustomField, Device, DevicePhoto


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


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        labels = {
            'vendor': 'Vendor',
            'model': 'Model',
            'hw': 'Hardware',
            'type': 'Type',
        }
        fields = ['vendor', 'model', 'hw', 'type']


class DevicePhotoForm(ModelForm):
    class Meta:
        model = DevicePhoto
        labels = {
            'device': 'Device',
            'photo': 'Photo',
            'desc': 'Description',
        }
        fields = ['device', 'photo', 'desc']
