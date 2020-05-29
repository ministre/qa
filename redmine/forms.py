from django.utils.translation import gettext_lazy as _
from django import forms


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
