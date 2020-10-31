from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm, HiddenInput
from docx_builder.models import DocxProfile


class DocxProfileForm(ModelForm):
    class Meta:
        model = DocxProfile
        labels = {
            'type': _('Type'),
            'name': _('Name'),
            'header_subtitle': _('Header Subtitle'),
            'header_logo': _('Header Logo'),

            'title_font_name': _('Name'),
            'title_font_size': _('Size') + ', [10-40]',
            'title_font_bold': _('Bold'),
            'title_font_italic': _('Italic'),
            'title_font_underline': _('Underline'),
            'title_font_color_red': _('Red') + ', [0-255]',
            'title_font_color_green': _('Green') + ', [0-255]',
            'title_font_color_blue': _('Blue') + ', [0-255]',
            'title_space_before': _('Space Before') + ', [0-40]',
            'title_space_after': _('Space After') + ', [0-40]',
            'title_alignment': _('Alignment'),

            'h1_font_name': _('Name'),
            'h1_font_size': _('Size') + ', [10-40]',
            'h1_font_bold': _('Bold'),
            'h1_font_italic': _('Italic'),
            'h1_font_underline': _('Underline'),
            'h1_font_color_red': _('Red') + ', [0-255]',
            'h1_font_color_green': _('Green') + ', [0-255]',
            'h1_font_color_blue': _('Blue') + ', [0-255]',
            'h1_space_before': _('Space Before') + ', [0-40]',
            'h1_space_after': _('Space After') + ', [0-40]',
            'h1_alignment': _('Alignment'),

            'h2_font_name': _('Name'),
            'h2_font_size': _('Size') + ', [10-40]',
            'h2_font_bold': _('Bold'),
            'h2_font_italic': _('Italic'),
            'h2_font_underline': _('Underline'),
            'h2_font_color_red': _('Red') + ', [0-255]',
            'h2_font_color_green': _('Green') + ', [0-255]',
            'h2_font_color_blue': _('Blue') + ', [0-255]',
            'h2_space_before': _('Space Before') + ', [0-40]',
            'h2_space_after': _('Space After') + ', [0-40]',
            'h2_alignment': _('Alignment'),

            'h3_font_name': _('Name'),
            'h3_font_size': _('Size') + ', [10-40]',
            'h3_font_bold': _('Bold'),
            'h3_font_italic': _('Italic'),
            'h3_font_underline': _('Underline'),
            'h3_font_color_red': _('Red') + ', [0-255]',
            'h3_font_color_green': _('Green') + ', [0-255]',
            'h3_font_color_blue': _('Blue') + ', [0-255]',
            'h3_space_before': _('Space Before') + ', [0-40]',
            'h3_space_after': _('Space After') + ', [0-40]',
            'h3_alignment': _('Alignment'),

            'normal_font_name': _('Name'),
            'normal_font_size': _('Size') + ', [10-40]',
            'normal_font_bold': _('Bold'),
            'normal_font_italic': _('Italic'),
            'normal_font_underline': _('Underline'),
            'normal_font_color_red': _('Red') + ', [0-255]',
            'normal_font_color_green': _('Green') + ', [0-255]',
            'normal_font_color_blue': _('Blue') + ', [0-255]',
            'normal_space_before': _('Space Before') + ', [0-40]',
            'normal_space_after': _('Space After') + ', [0-40]',
            'normal_alignment': _('Alignment'),

            'caption_font_name': _('Name'),
            'caption_font_size': _('Size') + ', [10-40]',
            'caption_font_bold': _('Bold'),
            'caption_font_italic': _('Italic'),
            'caption_font_underline': _('Underline'),
            'caption_font_color_red': _('Red') + ', [0-255]',
            'caption_font_color_green': _('Green') + ', [0-255]',
            'caption_font_color_blue': _('Blue') + ', [0-255]',
            'caption_space_before': _('Space Before') + ', [0-40]',
            'caption_space_after': _('Space After') + ', [0-40]',
            'caption_alignment': _('Alignment'),

            'quote_font_name': _('Name'),
            'quote_font_size': _('Size') + ', [10-40]',
            'quote_font_bold': _('Bold'),
            'quote_font_italic': _('Italic'),
            'quote_font_underline': _('Underline'),
            'quote_font_color_red': _('Red') + ', [0-255]',
            'quote_font_color_green': _('Green') + ', [0-255]',
            'quote_font_color_blue': _('Blue') + ', [0-255]',
            'quote_space_before': _('Space Before') + ', [0-40]',
            'quote_space_after': _('Space After') + ', [0-40]',
            'quote_alignment': _('Alignment'),
        }

        fields = '__all__'

        TYPE = (
            (0, 'Technical requirements'),
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
            'type': forms.Select(choices=TYPE, attrs={'class': 'form-control'}),

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

            'h3_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'h3_font_bold': forms.CheckboxInput,
            'h3_font_italic': forms.CheckboxInput,
            'h3_font_underline': forms.CheckboxInput,
            'h3_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),

            'normal_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'normal_font_bold': forms.CheckboxInput,
            'normal_font_italic': forms.CheckboxInput,
            'normal_font_underline': forms.CheckboxInput,
            'normal_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),

            'caption_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'caption_font_bold': forms.CheckboxInput,
            'caption_font_italic': forms.CheckboxInput,
            'caption_font_underline': forms.CheckboxInput,
            'caption_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),

            'quote_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'quote_font_bold': forms.CheckboxInput,
            'quote_font_italic': forms.CheckboxInput,
            'quote_font_underline': forms.CheckboxInput,
            'quote_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),

            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput(),
        }


class DocxTestplanForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=DocxProfile.objects.filter(type=1).order_by('id'))
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
    profile = forms.ModelChoiceField(queryset=DocxProfile.objects.filter(type=0).order_by('id'))


class DocxProtocolForm(forms.Form):
    protocol_id = forms.IntegerField()
    profile_id = forms.ModelChoiceField(queryset=DocxProfile.objects.all().order_by('id'))
    devices = forms.BooleanField(label=_('Devices information'), required=False)
    results_table = forms.BooleanField(label=_('Table of results'), required=False)
    issues = forms.BooleanField(label=_('List of issues'), required=False)
