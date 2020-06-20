from django.utils.translation import gettext_lazy as _
from django import forms


class DocxTestplanForm(forms.Form):
    purpose = forms.BooleanField(label=_('Purpose'), required=False)
