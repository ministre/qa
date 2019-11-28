from django.forms import ModelForm, HiddenInput
from .models import Pattern
from django.utils.translation import gettext_lazy as _


class PatternForm(ModelForm):
    class Meta:
        model = Pattern
        labels = {
            'name': _('Name'),
            'types': _('Device Types'),
            'redmine_url': _('Redmine URL'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
