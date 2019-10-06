from django.forms import ModelForm, HiddenInput
from testplan.models import TestplanPattern, TestplanPatternCategory, Testplan, TestplanCategory, TestplanChapter, Test
from django.utils.translation import gettext_lazy as _


class TestplanPatternForm(ModelForm):
    class Meta:
        model = TestplanPattern
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'


class TestplanPatternCategoryForm(ModelForm):
    class Meta:
        model = TestplanPatternCategory
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'pattern': HiddenInput(), 'queue': HiddenInput()}


class TestplanForm(ModelForm):
    class Meta:
        model = Testplan
        labels = {
            'name': _('Name'),
            'version': _('Version'),
            'device_type': _('Device Type'),
        }
        fields = ['name', 'version', 'device_type', 'created_by']
        widgets = {'created_by': HiddenInput()}


class TestplanCategoryForm(ModelForm):
    class Meta:
        model = TestplanCategory
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'testplan': HiddenInput()}


class TestplanChapterForm(ModelForm):
    class Meta:
        model = TestplanChapter
        labels = {
            'redmine_url': _('Redmine URL'),
            'name': _('Name'),
            'text': _('Text'),
        }
        fields = '__all__'
        widgets = {'testplan': HiddenInput()}


class TestForm(ModelForm):
    class Meta:
        model = Test
        labels = {
            'name': _('Name'),
            'purpose': _('Purpose'),
        }
        fields = '__all__'
        widgets = {'category': HiddenInput()}
