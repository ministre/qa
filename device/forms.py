from django.forms import ModelForm
from device.models import DeviceType


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'tag': 'Tag',
            'desc': 'Description',
        }
        fields = ['tag', 'desc']
