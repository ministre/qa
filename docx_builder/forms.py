from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm, HiddenInput
from docx_builder.models import DocxProfile


class DocxProfileForm(ModelForm):
    class Meta:
        model = DocxProfile
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DocxTestplanForm(forms.Form):
    purpose = forms.BooleanField(label=_('Purpose'), required=False)
