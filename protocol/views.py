from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Branch, Protocol, TestResult
from .forms import BranchForm, ProtocolForm
from django.urls import reverse
from testplan.models import Testplan, Category, Test
from device.models import Device, Sample, Firmware
from datetime import datetime
from django import forms
from django.shortcuts import get_object_or_404


class Item(object):
    @staticmethod
    def update_timestamp(foo, user):
        foo.updated_by = user
        foo.updated_at = datetime.now()
        foo.save()


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
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

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
    queryset = Protocol.objects.all()
    template_name = 'protocol/list.html'


@method_decorator(login_required, name='dispatch')
class ProtocolCreate(CreateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_form(self, form_class=ProtocolForm):
        form = super(ProtocolCreate, self).get_form(form_class)
        device = Device.objects.get(id=self.kwargs.get('device_id'))
        form.fields['firmware'].queryset = Firmware.objects.filter(device=device)
        form.fields['sample'].queryset = Sample.objects.filter(device=device)
        form.fields['testplan'].queryset = Testplan.objects.filter(device_type=device.type)
        form.fields['completed'].widget = forms.HiddenInput()
        form.fields['status'].widget = forms.HiddenInput()
        form.fields['scan'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        create_results(self.object)
        return reverse('protocol_details', kwargs={'pk': self.object.id})


def create_results(protocol: Protocol):
    for category in Category.objects.filter(testplan=protocol.testplan).order_by("-id"):
        for test in Test.objects.filter(category=category).order_by("-id"):
            new_result = TestResult(test=test, protocol=protocol)
            new_result.save()
    return True


@method_decorator(login_required, name='dispatch')
class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_form(self, form_class=ProtocolForm):
        form = super(ProtocolUpdate, self).get_form(form_class)
        device = Device.objects.get(id=self.kwargs.get('device_id'))
        form.fields['firmware'].queryset = Firmware.objects.filter(device=device)
        form.fields['sample'].queryset = Sample.objects.filter(device=device)
        form.fields['testplan'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class ProtocolDelete(DeleteView):
    model = Protocol
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 7})


def protocol_details(request, pk):
    protocol = get_object_or_404(Protocol, id=pk)
    results = TestResult.objects.filter(protocol=protocol).order_by('id')
    return render(request, 'protocol/details.html', {'protocol': protocol, 'results': results})
