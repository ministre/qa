from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm, HiddenInput
from docx_builder.models import DocxProfile


class DocxProfileForm(ModelForm):
    class Meta:
        model = DocxProfile
        labels = {
            'name': _('Name'),
            'logo': _('Logo'),
            'branch': _('Branch'),
            'title_font_name': _('Title Font Name'),
            'title_font_size': _('Title Font Size') + ', [10-40]',
            'title_font_bold': _('Title Font Bold'),
            'title_font_underline': _('Title Font Underline'),
            'title_font_color_red': _('Title Font Color Red') + ', [0-255]',
            'title_font_color_green': _('Title Font Color Green') + ', [0-255]',
            'title_font_color_blue': _('Title Font Color Blue') + ', [0-255]',
            'title_space_before': _('Title Font Space Before') + ', [0-40]',
            'title_space_after': _('Title Font Space After') + ', [0-40]',
            'heading1_font_name': _('Heading 1 Font Name'),
            'heading1_font_size': _('Heading 1 Font Size') + ', [10-40]',
            'heading1_font_bold': _('Heading 1 Font Bold'),
            'heading1_font_underline': _('Heading 1 Font Underline'),
            'heading1_font_color_red': _('Heading 1 Font Color Red') + ', [0-255]',
            'heading1_font_color_green': _('Heading 1 Font Color Green') + ', [0-255]',
            'heading1_font_color_blue': _('Heading 1 Font Color Blue') + ', [0-255]',
            'heading1_space_before': _('Heading 1 Font Space Before') + ', [0-40]',
            'heading1_space_after': _('Heading 1 Font Space After') + ', [0-40]',
        }
        fields = '__all__'
        FONTNAME = (
            ('Calibri', 'Calibri'),
            ('Cambria', 'Cambria'),
        )
        widgets = {
            'title_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'heading1_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'title_font_bold': forms.CheckboxInput,
            'heading1_font_bold': forms.CheckboxInput,
            'title_font_underline': forms.CheckboxInput,
            'heading1_font_underline': forms.CheckboxInput,
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput(),
        }


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
