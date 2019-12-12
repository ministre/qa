from django.forms import ModelForm, HiddenInput
from .models import FeatureList
from django.utils.translation import gettext_lazy as _


class FeatureListForm(ModelForm):
    class Meta:
        model = FeatureList
        labels = {
            'device_type': _('Device Type'),
            'name': _('Name'),
            'version': _('Version'),
            'redmine_url': _('Redmine URL'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
