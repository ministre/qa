from django.utils.translation import gettext_lazy as _
from django import forms


class RedmineChapterForm(forms.Form):
    project = forms.CharField(label='Project', max_length=100)
    wiki = forms.CharField(label='Wiki', max_length=100)


class RedmineTestForm(forms.Form):
    project = forms.CharField(label='Project', max_length=100)
    wiki = forms.CharField(label='Wiki', max_length=100)
    purpose = forms.BooleanField(label=_('Purpose'), required=False)
    procedure = forms.BooleanField(label=_('Procedure'), required=False)
    configs = forms.BooleanField(label=_('Configurations'), required=False)
    images = forms.BooleanField(label=_('Images'), required=False)
    files = forms.BooleanField(label=_('Files'), required=False)
    expected = forms.BooleanField(label=_('Expected result'), required=False)
    checklists = forms.BooleanField(label=_('Checklists'), required=False)
    links = forms.BooleanField(label=_('Links'), required=False)
    comments = forms.BooleanField(label=_('Comments'), required=False)


class RedmineExportTestplanForm(forms.Form):
    parent = forms.CharField(label=_('Parent Project'), max_length=100)
    project = forms.CharField(label=_('Project'), max_length=100)
    chapters = forms.BooleanField(label=_('Chapters'), required=False)
    tests = forms.BooleanField(label=_('Tests'), required=False)


class RedmineImportTestplanForm(forms.Form):
    project = forms.CharField(label=_('Project'), max_length=100)
    chapters = forms.BooleanField(label=_('Chapters'), required=False)
    tests = forms.BooleanField(label=_('Tests'), required=False)


class RedmineFeatureListForm(forms.Form):
    project = forms.CharField(label='Project', max_length=100)
    wiki = forms.CharField(label='Wiki', max_length=100)


class ExportDeviceTypeForm(forms.Form):
    parent = forms.CharField(label=_('Parent Project'), max_length=100)
    project = forms.CharField(label=_('Project'), max_length=100)
    project_name = forms.CharField(label=_('Project Name'), max_length=1000)
    specs = forms.BooleanField(label=_('Specifications'), required=False)
    tech_reqs = forms.BooleanField(label=_('Technical Requirements'), required=False)


class ImportDeviceTypeForm(forms.Form):
    project = forms.CharField(label=_('Project'), max_length=100)
