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
        FONTNAME = (
            ('Calibri', 'Calibri'),
            ('Cambria', 'Cambria'),
        )
        widgets = {'title_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput(),
                   'title_font_bold': forms.CheckboxInput,
                   'title_font_underline': forms.CheckboxInput}


class DocxTestplanForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=DocxProfile.objects.all())
    page_header = forms.BooleanField(label=_('Page Header'), required=False)
    convert_textile = forms.BooleanField(label=_('Convert Textile'), required=False)
    chapters = forms.BooleanField(label=_('Chapters'), required=False)
    purpose = forms.BooleanField(label=_('Purpose'), required=False)
    procedure = forms.BooleanField(label=_('Procedure'), required=False)
    expected = forms.BooleanField(label=_('Expected'), required=False)
    configs = forms.BooleanField(label=_('Configs'), required=False)
    images = forms.BooleanField(label=_('Images'), required=False)
    checklists = forms.BooleanField(label=_('Checklists'), required=False)
    links = forms.BooleanField(label=_('Links'), required=False)
    comments = forms.BooleanField(label=_('Comments'), required=False)
