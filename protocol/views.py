from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Branch, Protocol, ProtocolDevice
from device.models import Firmware, DeviceSample
from .forms import BranchForm, ProtocolForm, ProtocolDeviceForm
from django.urls import reverse
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
    queryset = Protocol.objects.all().order_by('id')
    template_name = 'protocol/protocols.html'


@method_decorator(login_required, name='dispatch')
class ProtocolCreate(CreateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

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
        return reverse('protocols')


@method_decorator(login_required, name='dispatch')
class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocols')
        return context

    def get_success_url(self):
        return reverse('protocols')


@method_decorator(login_required, name='dispatch')
class ProtocolDelete(DeleteView):
    model = Protocol
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocols')
        return context

    def get_success_url(self):
        return reverse('protocols')


def protocol_details(request, pk, tab_id):
    protocol = get_object_or_404(Protocol, id=pk)
    protocol_devices = ProtocolDevice.objects.filter(protocol=protocol).order_by('id')
    return render(request, 'protocol/protocol_details.html', {'protocol': protocol,
                                                              'protocol_devices': protocol_devices, 'tab_id': tab_id})


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
        return reverse('protocol_details', kwargs={'pk': self.kwargs.get('p_id'), 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceUpdate(UpdateView):
    model = ProtocolDevice
    form_class = ProtocolDeviceForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'firmware': None, 'sample': None, 'updated_by': self.request.user, 'updated_at': datetime.now}

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
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceFwUpdate(UpdateView):
    model = ProtocolDevice
    form_class = ProtocolDeviceForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

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
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ProtocolDeviceSampleUpdate(UpdateView):
    model = ProtocolDevice
    form_class = ProtocolDeviceForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

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
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})
