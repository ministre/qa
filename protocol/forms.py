from django.forms import ModelForm, HiddenInput
from .models import Branch, Protocol, ProtocolDevice, ProtocolScan, ProtocolTestResult, TestResultIssue, \
    TestResultComment, TestResultImage
from django.utils.translation import gettext_lazy as _
from django import forms


class BranchForm(ModelForm):
    class Meta:
        model = Branch
        labels = {
            'name': _('Branch'),
        }
        fields = '__all__'
        widgets = {
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        labels = {
            'testplan': _('Testplan'),
            'started': _('Started'),
            'completed': _('Completed'),
            'status': _('Status'),
        }
        fields = '__all__'
        STATUS = (
            ('0', 'In progress'),
            ('1', 'Not recommended'),
            ('2', 'Limited'),
            ('3', 'Recommended'),
        )
        widgets = {
            'status': forms.Select(choices=STATUS, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolDeviceForm(ModelForm):
    class Meta:
        model = ProtocolDevice
        labels = {
            'device': _('Device'),
            'firmware': _('Firmware'),
            'sample': _('Sample'),
        }
        fields = '__all__'
        widgets = {
            'protocol': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolScanForm(ModelForm):
    class Meta:
        model = ProtocolScan
        labels = {
            'scan': _('Scan'),
        }
        fields = '__all__'
        widgets = {
            'protocol': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolTestResultForm(ModelForm):
    class Meta:
        model = ProtocolTestResult
        labels = {
            'result': _('Result'),
        }
        fields = '__all__'
        RESULT = (
            ('1', 'Not tested'),
            ('2', 'Failed'),
            ('3', 'Warning'),
            ('4', 'Success'),
        )
        widgets = {
            'protocol': HiddenInput(), 'test': HiddenInput(),
            'result': forms.Select(choices=RESULT, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestResultIssueForm(ModelForm):
    class Meta:
        model = TestResultIssue
        labels = {
            'text': _('Text'),
            'ticket': _('Ticket'),
        }
        fields = '__all__'
        widgets = {
            'result': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestResultCommentForm(ModelForm):
    class Meta:
        model = TestResultComment
        labels = {
            'text': _('Text'),
        }
        fields = '__all__'
        widgets = {
            'result': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestResultImageForm(ModelForm):
    class Meta:
        model = TestResultImage
        labels = {
            'desc': _('Description'),
            'image': _('Image'),
            'width': _('Width'),
            'height': _('Height'),
        }
        fields = '__all__'
        widgets = {
            'result': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
