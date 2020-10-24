from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Branch, Protocol, ProtocolDevice, ProtocolScan, ProtocolTestResult, TestResultIssue, \
    TestResultComment, TestResultImage
from device.models import Firmware, DeviceSample
from testplan.models import Category, Test
from .forms import BranchForm, ProtocolForm, ProtocolDeviceForm, ProtocolScanForm, ProtocolTestResultForm, \
    TestResultIssueForm, TestResultCommentForm, TestResultImageForm
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.shortcuts import get_object_or_404
from device.views import Item
from django.http import HttpResponseRedirect


@method_decorator(login_required, name='dispatch')
class BranchListView(ListView):
    context_object_name = 'branches'
    queryset = Branch.objects.all().order_by('id')
    template_name = 'protocol/branches.html'


@method_decorator(login_required, name='dispatch')
class BranchCreate(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('branches')
        return context

    def get_success_url(self):
        return reverse('branches')


@method_decorator(login_required, name='dispatch')
class BranchUpdate(UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('branches')
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('branches')


@method_decorator(login_required, name='dispatch')
class BranchDelete(DeleteView):
    model = Branch
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('branches')
        return context

    def get_success_url(self):
        return reverse('branches')


@method_decorator(login_required, name='dispatch')
class ProtocolListView(ListView):
    context_object_name = 'protocols'
    queryset = Protocol.objects.all().order_by('id')
    template_name = 'protocol/protocols.html'


@method_decorator(login_required, name='dispatch')
class ProtocolCreate(CreateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_form(self, form_class=ProtocolForm):
        form = super(ProtocolCreate, self).get_form(form_class)
        form.fields['completed'].widget = forms.HiddenInput()
        form.fields['status'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocols')
        return context

    def get_success_url(self):
        return reverse('protocol_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('protocol_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class ProtocolDelete(DeleteView):
    model = Protocol
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('protocols')


def protocol_details(request, pk, tab_id):
    protocol = get_object_or_404(Protocol, id=pk)
    protocol_devices = ProtocolDevice.objects.filter(protocol=protocol).order_by('id')
    protocol_test_results = get_protocol_test_results(protocol)
    protocol_scans = ProtocolScan.objects.filter(protocol=protocol).order_by('id')
    return render(request, 'protocol/protocol_details.html', {'protocol': protocol,
                                                              'protocol_devices': protocol_devices,
                                                              'protocol_test_results': protocol_test_results,
                                                              'protocol_scans': protocol_scans,
                                                              'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceCreate(CreateView):
    model = ProtocolDevice
    form_class = ProtocolDeviceForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'protocol': self.kwargs.get('p_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_form(self, form_class=ProtocolDeviceForm):
        form = super(ProtocolDeviceCreate, self).get_form(form_class)
        form.fields['firmware'].widget = forms.HiddenInput()
        form.fields['sample'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.kwargs.get('p_id'), 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.kwargs.get('p_id'), 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceUpdate(UpdateView):
    model = ProtocolDevice
    form_class = ProtocolDeviceForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'firmware': None, 'sample': None, 'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_form(self, form_class=ProtocolDeviceForm):
        form = super(ProtocolDeviceUpdate, self).get_form(form_class)
        form.fields['firmware'].widget = forms.HiddenInput()
        form.fields['sample'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceFwUpdate(UpdateView):
    model = ProtocolDevice
    form_class = ProtocolDeviceForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_form(self, form_class=ProtocolDeviceForm):
        form = super(ProtocolDeviceFwUpdate, self).get_form(form_class)
        form.fields['device'].widget = forms.HiddenInput()
        form.fields['sample'].widget = forms.HiddenInput()
        form.fields['firmware'].queryset = Firmware.objects.filter(device=self.object.device).order_by('id')
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceSampleUpdate(UpdateView):
    model = ProtocolDevice
    form_class = ProtocolDeviceForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_form(self, form_class=ProtocolDeviceForm):
        form = super(ProtocolDeviceSampleUpdate, self).get_form(form_class)
        form.fields['device'].widget = forms.HiddenInput()
        form.fields['firmware'].widget = forms.HiddenInput()
        form.fields['sample'].queryset = DeviceSample.objects.filter(device=self.object.device).order_by('id')
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceDelete(DeleteView):
    model = ProtocolDevice
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolScanCreate(CreateView):
    model = ProtocolScan
    form_class = ProtocolScanForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'protocol': self.kwargs.get('p_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.kwargs.get('p_id'), 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.kwargs.get('p_id'), 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class ProtocolScanUpdate(UpdateView):
    model = ProtocolScan
    form_class = ProtocolScanForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class ProtocolScanDelete(DeleteView):
    model = ProtocolScan
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 3})


def get_protocol_test_results(protocol: Protocol):
    results = []
    l1_num = 0
    categories = Category.objects.filter(testplan=protocol.testplan).order_by('priority')
    for category in categories:
        l1_num += 1
        l2_num = 0
        tests = Test.objects.filter(category=category).order_by('priority')
        for test in tests:
            l2_num += 1
            status = 0
            result_id = 0
            test_issues = []
            test_comments = []
            images_count = 0
            test_results = ProtocolTestResult.objects.filter(protocol=protocol, test=test)
            for test_result in test_results:
                status = test_result.result
                result_id = test_result.id

                issues = TestResultIssue.objects.filter(result=test_result)
                for issue in issues:
                    test_issues.append({'text': issue.text, 'ticket': issue.ticket})

                comments = TestResultComment.objects.filter(result=test_result)
                for comment in comments:
                    test_comments.append(comment.text)

                images_count = TestResultImage.objects.filter(result=test_result).count

            result = {'l1_num': l1_num, 'l2_num': l2_num,
                      'category_id': category.id, 'category_name': category.name,
                      'test_id': test.id, 'test_name': test.name, 'status': status, 'result_id': result_id,
                      'test_issues': test_issues, 'test_comments': test_comments,
                      'test_images_count': images_count}
            results.append(result)
    return results


@login_required
def protocol_test_result_create(request, protocol_id: int, test_id: int):
    protocol = get_object_or_404(Protocol, id=protocol_id)
    test = get_object_or_404(Test, id=test_id)
    protocol_test_result, create = ProtocolTestResult.objects.update_or_create(protocol=protocol, test=test,
                                                                               defaults={'created_by': request.user,
                                                                                         'updated_by': request.user})
    return HttpResponseRedirect(reverse('protocol_test_result_details', kwargs={'pk': protocol_test_result.id,
                                                                                'tab_id': 6}))


@method_decorator(login_required, name='dispatch')
class ProtocolTestResultDelete(DeleteView):
    model = ProtocolTestResult
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 3})


@login_required
def protocol_test_result_details(request, pk, tab_id):
    test_result = get_object_or_404(ProtocolTestResult, id=pk)
    if request.method == "POST":
        form = ProtocolTestResultForm(request.POST, instance=test_result)
        if form.is_valid():
            test = form.save(commit=False)
            test.updated_at = timezone.now()
            test.updated_by = request.user
            test.save()
        return HttpResponseRedirect(reverse('protocol_test_result_details', kwargs={'pk': pk, 'tab_id': 6}))
    else:
        form = ProtocolTestResultForm(instance=test_result)
        return render(request, 'protocol/test_result_details.html', {'test_result': test_result, 'tab_id': tab_id,
                                                                     'form': form})


@method_decorator(login_required, name='dispatch')
class TestResultIssueCreate(CreateView):
    model = TestResultIssue
    form_class = TestResultIssueForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('tr'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.kwargs.get('tr'), 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.kwargs.get('tr'), 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestResultIssueUpdate(UpdateView):
    model = TestResultIssue
    form_class = TestResultIssueForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestResultIssueDelete(DeleteView):
    model = TestResultIssue
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestResultCommentCreate(CreateView):
    model = TestResultComment
    form_class = TestResultCommentForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('tr'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.kwargs.get('tr'), 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.kwargs.get('tr'), 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestResultCommentUpdate(UpdateView):
    model = TestResultComment
    form_class = TestResultCommentForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestResultCommentDelete(DeleteView):
    model = TestResultComment
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestResultImageCreate(CreateView):
    model = TestResultImage
    form_class = TestResultImageForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('tr'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.kwargs.get('tr'), 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.kwargs.get('tr'), 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class TestResultImageUpdate(UpdateView):
    model = TestResultImage
    form_class = TestResultImageForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class TestResultImageDelete(DeleteView):
    model = TestResultImage
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('protocol_test_result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})
