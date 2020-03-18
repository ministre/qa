from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Protocol
from .forms import ProtocolForm
from django.urls import reverse
from firmware.models import Firmware
from testplan.models import Testplan
from device.models import Device


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
        form.fields['testplan'].queryset = Testplan.objects.filter(device_type=device.type)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('protocols')
        # return reverse('protocol_details', kwargs={'pk': self.kwargs.get('device_id')})
