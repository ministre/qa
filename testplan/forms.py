from django.forms import ModelForm
from testplan.models import TestplanPattern
from django.utils.translation import gettext_lazy as _


class TestplanPatternForm(ModelForm):
    class Meta:
        model = TestplanPattern
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
