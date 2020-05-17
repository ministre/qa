from django.forms import ModelForm, HiddenInput
from testplan.models import Testplan, Category, Chapter, Test, TestConfig, TestImage, TestFile,\
    TestWorksheet, TestWorksheetItem, TestChecklist, TestChecklistItem, TestLink, TestComment, Pattern
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


class TestWorksheetForm(ModelForm):
    class Meta:
        model = TestWorksheet
        labels = {
            'name': _('Name'),
            'type': _('Value Type'),
        }
        fields = '__all__'
        TYPE = (
            ('text', 'Text'),
            ('number', 'Number'),
            ('checklist', 'Checklist'),
            ('table', 'Table'),
        )
        widgets = {
            'type': forms.Select(choices=TYPE, attrs={'class': 'form-control'}),
            'test': HiddenInput()
        }


class WorksheetItemForm(ModelForm):
    class Meta:
        model = TestWorksheetItem
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'

        widgets = {
            'worksheet': HiddenInput()
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


class PatternForm(ModelForm):
    class Meta:
        model = Pattern
        labels = {
            'name': _('Name'),
            'types': _('Device Types'),
            'redmine_parent': _('Redmine Parent Project ID'),
            'redmine_project': _('Redmine Project ID'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(PatternForm, self).__init__(*args, **kwargs)
        self.fields['redmine_parent'].initial = 'patterns'


class RedmineForm(forms.Form):
    project = forms.CharField(label='Project', max_length=100)
    wiki = forms.CharField(label='Wiki', max_length=100)
    name = forms.BooleanField(label=_('Name'), required=False)
    purpose = forms.BooleanField(label=_('Purpose'), required=False)
    procedure = forms.BooleanField(label=_('Procedure'), required=False)
    expected = forms.BooleanField(label=_('Expected result'), required=False)
    configs = forms.BooleanField(label=_('Configurations'), required=False)
    images = forms.BooleanField(label=_('Images'), required=False)
    files = forms.BooleanField(label=_('Files'), required=False)
    checklists = forms.BooleanField(label=_('Checklists'), required=False)
    links = forms.BooleanField(label=_('Links'), required=False)
    comments = forms.BooleanField(label=_('Comments'), required=False)
