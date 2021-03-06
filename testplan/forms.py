from django.forms import ModelForm, HiddenInput
from testplan.models import Testplan, Category, Chapter, Test, TestConfig, TestImage, TestFile, TestChecklist, \
    TestChecklistItem, TestIntegerValue, TestLink, TestComment
from django.utils.translation import gettext_lazy as _
from django import forms


class TestplanForm(ModelForm):
    class Meta:
        model = Testplan
        labels = {
            'name': _('Name'),
            'version': _('Document version'),
            'device_type': _('Device Type'),
            'redmine_parent': _('Redmine Parent Project ID'),
            'redmine_project': _('Redmine Project ID'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(TestplanForm, self).__init__(*args, **kwargs)
        self.fields['redmine_parent'].initial = 'testplans'


class TestplanCategoryForm(ModelForm):
    class Meta:
        model = Category
        labels = {
            'name': _('Name'),
            'priority': _('Priority'),
        }
        fields = '__all__'
        widgets = {'testplan': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        labels = {
            'redmine_wiki': _('Redmine wiki'),
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
            'redmine_wiki': _('Redmine Wiki'),
        }
        fields = '__all__'
        widgets = {'category': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
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
            'width': _('Width'),
            'height': _('Height'),
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


class TestChecklistItemForm(ModelForm):
    class Meta:
        model = TestChecklistItem
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {
            'checklist': HiddenInput()
        }


class TestIntegerValueForm(ModelForm):
    class Meta:
        model = TestIntegerValue
        labels = {
            'name': _('Name'),
            'unit': _('Unit'),
        }
        fields = '__all__'
        widgets = {
            'test': HiddenInput()
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


class TestCommentForm(ModelForm):
    class Meta:
        model = TestComment
        labels = {
            'text': _('Text'),
        }
        fields = '__all__'

        widgets = {
            'test': HiddenInput()
        }
