from django.forms import ModelForm, HiddenInput
from device.models import Vendor, DeviceChecklist, DeviceChecklistItem, DeviceSlist, DeviceSlistItem, \
    DeviceTextField, DeviceIntegerField, DeviceType, DeviceTypeSpecification, Device, DeviceDocumentType, \
    DeviceDocument, DevicePhoto, DeviceSample, DeviceSampleAccount, Firmware, FirmwareAccount, FirmwareFile, \
    FirmwareScreenshot, FirmwareHowto, DeviceSupport
from django.utils.translation import gettext_lazy as _
from django import forms


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceChecklistForm(ModelForm):
    class Meta:
        model = DeviceChecklist
        labels = {
            'name': _('Name'),
            'desc': _('Description'),
            'items_order_by': _('Sort items by'),
        }
        fields = '__all__'
        ORDER_BY = (
            ('id', 'ID'),
            ('name', 'Name'),
        )
        widgets = {
            'items_order_by': forms.Select(choices=ORDER_BY, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class DeviceChecklistItemForm(ModelForm):
    class Meta:
        model = DeviceChecklistItem
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'checklist': HiddenInput()}


class DeviceSlistForm(ModelForm):
    class Meta:
        model = DeviceSlist
        labels = {
            'name': _('Name'),
            'desc': _('Description'),
            'items_order_by': _('Sort items by'),
        }
        fields = '__all__'
        ORDER_BY = (
            ('id', 'ID'),
            ('name', 'Name'),
        )
        widgets = {
            'items_order_by': forms.Select(choices=ORDER_BY, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class DeviceSlistItemForm(ModelForm):
    class Meta:
        model = DeviceSlistItem
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'slist': HiddenInput()}


class DeviceTextFieldForm(ModelForm):
    class Meta:
        model = DeviceTextField
        labels = {
            'name': _('Name'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class DeviceIntegerFieldForm(ModelForm):
    class Meta:
        model = DeviceIntegerField
        labels = {
            'name': _('Name'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'tag': _('Tag'),
            'desc': _('Description'),
            'desc_genitive': _('Genitive Description'),
            'redmine_parent': _('Redmine Parent Project ID'),
            'redmine_project': _('Redmine Project ID'),
            'redmine_project_name': _('Redmine Project Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceTypeSpecificationForm(ModelForm):
    class Meta:
        model = DeviceTypeSpecification
        labels = {
            'checklist': _('Checkbox'),
            'slist': _('Dropdown Menu'),
            'text_field': _('Text Field'),
            'integer_field': _('Integer Field'),
        }
        fields = '__all__'
        widgets = {'type': HiddenInput()}


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        labels = {
            'type': _('Type'),
            'vendor': _('Vendor'),
            'model': _('Model'),
            'hw': _('Hardware'),
            'redmine_project': _('Redmine Project ID'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceDocumentTypeForm(ModelForm):
    class Meta:
        model = DeviceDocumentType
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceDocumentForm(ModelForm):
    class Meta:
        model = DeviceDocument
        labels = {
            'file': _('Document File'),
            'type': _('Document Type'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DevicePhotoForm(ModelForm):
    class Meta:
        model = DevicePhoto
        labels = {
            'photo': _('Photo'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceSampleForm(ModelForm):
    class Meta:
        model = DeviceSample
        labels = {
            'sn': _('Serial Number'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceSampleAccountForm(ModelForm):
    class Meta:
        model = DeviceSampleAccount
        labels = {
            'username': _('Username'),
            'password': _('Password'),
        }
        fields = '__all__'
        widgets = {'sample': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class FirmwareForm(ModelForm):
    class Meta:
        model = Firmware
        labels = {
            'version': _('FW Version'),
            'checksum': _('Checksum'),
            'sysinfo': _('System Information'),
            'description': _('Description'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class FirmwareAccountForm(ModelForm):
    class Meta:
        model = FirmwareAccount
        labels = {
            'username': _('Username'),
            'password': _('Password'),
            'description': _('Description'),
        }
        fields = '__all__'
        widgets = {'firmware': HiddenInput()}


class FirmwareFileForm(ModelForm):
    class Meta:
        model = FirmwareFile
        labels = {
            'file': _('File'),
            'description': _('Description'),
        }
        fields = '__all__'
        widgets = {'firmware': HiddenInput()}


class FirmwareScreenshotForm(ModelForm):
    class Meta:
        model = FirmwareScreenshot
        labels = {
            'image': _('File'),
            'description': _('Description'),
        }
        fields = '__all__'
        widgets = {'firmware': HiddenInput()}


class FirmwareHowtoForm(ModelForm):
    class Meta:
        model = FirmwareHowto
        labels = {
            'name': _('Name'),
            'text': _('Text'),
        }
        fields = '__all__'
        widgets = {'firmware': HiddenInput()}


class DeviceSupportForm(ModelForm):
    class Meta:
        model = DeviceSupport
        labels = {
            'contact': _('Contact'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
