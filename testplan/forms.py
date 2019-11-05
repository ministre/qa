from django.forms import ModelForm, HiddenInput
from testplan.models import Testplan, Category, Chapter, Test
from django.utils.translation import gettext_lazy as _


class TestplanForm(ModelForm):
    class Meta:
        model = Testplan
        labels = {
            'name': _('Name'),
            'version': _('Document version'),
            'device_type': _('Device Type'),
            'redmine_url': _('Redmine URL'),
        }
        fields = ['name', 'version', 'device_type', 'redmine_url', 'created_by', 'created_at',
                  'updated_by', 'updated_at']
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'testplan': HiddenInput()}


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        labels = {
            'redmine_url': _('Redmine URL'),
            'name': _('Name'),
            'text': _('Text'),
        }
        fields = '__all__'
        widgets = {'testplan': HiddenInput(), 'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class TestForm(ModelForm):
    class Meta:
        model = Test
        labels = {
            'name': _('Name'),
            'purpose': _('Purpose'),
            'procedure': _('Procedure'),
            'expected': _('Expected result'),
            'redmine_url': _('Redmine URL'),
        }
        fields = '__all__'
        widgets = {'category': HiddenInput()}
