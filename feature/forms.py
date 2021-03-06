from django.forms import ModelForm, HiddenInput
from .models import FeatureList, FeatureListCategory, FeatureListItem, FeatureListFile, FeatureListLink
from django.utils.translation import gettext_lazy as _


class FeatureListForm(ModelForm):
    class Meta:
        model = FeatureList
        labels = {
            'device_type': _('Device Type'),
            'name': _('Name'),
            'version': _('Version'),
            'redmine_wiki': _('Redmine Wiki'),
        }
        fields = '__all__'
        widgets = {'device_type': HiddenInput(), 'redmine_wiki': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(FeatureListForm, self).__init__(*args, **kwargs)
        self.fields['redmine_wiki'].initial = 'technical_requirements'


class FeatureListCategoryForm(ModelForm):
    class Meta:
        model = FeatureListCategory
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'feature_list': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class FeatureListItemForm(ModelForm):
    class Meta:
        model = FeatureListItem
        labels = {
            'name': _('Name'),
            'optional': _('Optional'),
        }
        fields = '__all__'
        widgets = {'category': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class FeatureListFileForm(ModelForm):
    class Meta:
        model = FeatureListFile
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'feature_list': HiddenInput()}


class FeatureListLinkForm(ModelForm):
    class Meta:
        model = FeatureListLink
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'feature_list': HiddenInput()}
