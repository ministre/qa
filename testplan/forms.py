from django.forms import ModelForm, HiddenInput
from testplan.models import Testplan, Category, Chapter, Test, TestConfig, TestImage, TestFile, TestChecklist, \
    ChecklistItem, TestLink, Pattern
from django.utils.translation import gettext_lazy as _
from django import forms


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
        widgets = {'category': HiddenInput(), 'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class TestConfigForm(ModelForm):
    class Meta:
        model = TestConfig
        labels = {
            'name': _('Name'),
            'lang': _('Style'),
            'config': _('Configuration'),
        }
        fields = '__all__'
        LANG = (
            ('json', 'JSON'),
            ('c', 'C'),
            ('coffee', 'Coffeescript'),
            ('csharp', 'C#'),
            ('css', 'CSS'),
            ('d', 'D'),
            ('go', 'Go'),
            ('haskell', 'Haskell'),
            ('html', 'HTML'),
            ('javascript', 'JavaScript'),
            ('lua', 'Lua'),
            ('php', 'PHP'),
            ('python', 'Python'),
            ('r', 'R'),
            ('ruby', 'Ruby'),
            ('scheme', 'Scheme'),
            ('shell', 'Shell'),
        )

        widgets = {
            'lang': forms.Select(choices=LANG, attrs={'class': 'form-control'}),
            'test': HiddenInput()
        }


class TestImageForm(ModelForm):
    class Meta:
        model = TestImage
        labels = {
            'name': _('Name'),
            'image': _('Image'),
        }
        fields = '__all__'

        widgets = {
            'test': HiddenInput()
        }


class TestFileForm(ModelForm):
    class Meta:
        model = TestFile
        labels = {
            'name': _('Name'),
            'file': _('File'),
        }
        fields = '__all__'

        widgets = {
            'test': HiddenInput()
        }


class TestChecklistForm(ModelForm):
    class Meta:
        model = TestChecklist
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'

        widgets = {
            'test': HiddenInput()
        }


class ChecklistItemForm(ModelForm):
    class Meta:
        model = ChecklistItem
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'

        widgets = {
            'checklist': HiddenInput()
        }


class TestLinkForm(ModelForm):
    class Meta:
        model = TestLink
        labels = {
            'name': _('Name'),
            'url': _('URL'),
        }
        fields = '__all__'

        widgets = {
            'test': HiddenInput()
        }


# patterns

class PatternForm(ModelForm):
    class Meta:
        model = Pattern
        labels = {
            'name': _('Name'),
            'device_types': _('Device Types'),
            'redmine_url': _('Redmine URL'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
