from django.forms import ModelForm, HiddenInput
from .models import Pattern, PatternCategory
from django.utils.translation import gettext_lazy as _


class PatternForm(ModelForm):
    class Meta:
        model = Pattern
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class PatternCategoryForm(ModelForm):
    class Meta:
        model = PatternCategory
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
