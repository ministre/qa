from django.forms import ModelForm, HiddenInput
from docum.models import DocumType
from django.utils.translation import gettext_lazy as _


class DocumTypeForm(ModelForm):
    class Meta:
        model = DocumType
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
