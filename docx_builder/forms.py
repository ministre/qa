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
            'header_subtitle': _('Header Subtitle'),

            'title_font_name': _('Title Font Name'),
            'title_font_size': _('Title Font Size') + ', [10-40]',
            'title_font_bold': _('Title Font Bold'),
            'title_font_italic': _('Title Font Italic'),
            'title_font_underline': _('Title Font Underline'),
            'title_font_color_red': _('Title Font Color Red') + ', [0-255]',
            'title_font_color_green': _('Title Font Color Green') + ', [0-255]',
            'title_font_color_blue': _('Title Font Color Blue') + ', [0-255]',
            'title_space_before': _('Title Font Space Before') + ', [0-40]',
            'title_space_after': _('Title Font Space After') + ', [0-40]',
            'title_alignment': _('Title Alignment') + ', [0-40]',

            'h1_font_name': _('Heading 1 Font Name'),
            'h1_font_size': _('Heading 1 Font Size') + ', [10-40]',
            'h1_font_bold': _('Heading 1 Font Bold'),
            'h1_font_italic': _('Heading 1 Font Italic'),
            'h1_font_underline': _('Heading 1 Font Underline'),
            'h1_font_color_red': _('Heading 1 Font Color Red') + ', [0-255]',
            'h1_font_color_green': _('Heading 1 Font Color Green') + ', [0-255]',
            'h1_font_color_blue': _('Heading 1 Font Color Blue') + ', [0-255]',
            'h1_space_before': _('Heading 1 Font Space Before') + ', [0-40]',
            'h1_space_after': _('Heading 1 Font Space After') + ', [0-40]',
            'h1_alignment': _('Heading 1 Alignment') + ', [0-40]',

            'h2_font_name': _('Heading 2 Font Name'),
            'h2_font_size': _('Heading 2 Font Size') + ', [10-40]',
            'h2_font_bold': _('Heading 2 Font Bold'),
            'h2_font_italic': _('Heading 2 Font Italic'),
            'h2_font_underline': _('Heading 2 Font Underline'),
            'h2_font_color_red': _('Heading 2 Font Color Red') + ', [0-255]',
            'h2_font_color_green': _('Heading 2 Font Color Green') + ', [0-255]',
            'h2_font_color_blue': _('Heading 2 Font Color Blue') + ', [0-255]',
            'h2_space_before': _('Heading 2 Font Space Before') + ', [0-40]',
            'h2_space_after': _('Heading 2 Font Space After') + ', [0-40]',
            'h2_alignment': _('Heading 1 Alignment') + ', [0-40]',
        }

        fields = '__all__'

        TYPE = (
            (0, 'Feature List'),
            (1, 'Testplan'),
            (2, 'Protocol'),
        )

        FONTNAME = (
            ('Calibri', 'Calibri'),
            ('Cambria', 'Cambria'),
        )

        ALIGNMENT = (
            (0, 'Left'),
            (1, 'Center'),
            (2, 'Right'),
            (3, 'Justify'),
        )

        widgets = {
            'title_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'title_font_bold': forms.CheckboxInput,
            'title_font_italic': forms.CheckboxInput,
            'title_font_underline': forms.CheckboxInput,
            'title_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),

            'h1_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'h1_font_bold': forms.CheckboxInput,
            'h1_font_italic': forms.CheckboxInput,
            'h1_font_underline': forms.CheckboxInput,
            'h1_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),

            'h2_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'h2_font_bold': forms.CheckboxInput,
            'h2_font_italic': forms.CheckboxInput,
            'h2_font_underline': forms.CheckboxInput,
            'h2_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),

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


class DocxFeatureListForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=DocxProfile.objects.all())
