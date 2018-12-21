from django.shortcuts import render
from device.models import DeviceType
from .forms import DeviceTypeForm
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse


class DeviceTypeListView(ListView):
    context_object_name = 'device_types'
    queryset = DeviceType.objects.all()
    template_name = 'device/device_type_list.html'


class DeviceTypeCreate(CreateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/device_type_create.html'

    def get_success_url(self):
        return reverse('device_type_list')


class DeviceTypeUpdate(UpdateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/device_type_update.html'

    def get_success_url(self):
        return reverse('device_type_list')


class DeviceTypeDelete(DeleteView):
    model = DeviceType
    template_name = 'device/device_type_delete.html'

    def get_success_url(self):
        return reverse('device_type_list')


def device_list(request):
    return render(request, 'device/device_list.html')
