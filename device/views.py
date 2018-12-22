from django.shortcuts import render
from device.models import CustomField, DeviceType, Device
from .forms import CustomFieldForm, DeviceTypeForm, DeviceForm
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse


class CustomFieldListView(ListView):
    context_object_name = 'custom_fields'
    queryset = CustomField.objects.all()
    template_name = 'device/custom_field_list.html'


class CustomFieldCreate(CreateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = 'device/custom_field_create.html'

    def get_success_url(self):
        return reverse('custom_field_list')


class CustomFieldUpdate(UpdateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = 'device/custom_field_update.html'

    def get_success_url(self):
        return reverse('custom_field_list')


class CustomFieldDelete(DeleteView):
    model = CustomField
    template_name = 'device/custom_field_delete.html'

    def get_success_url(self):
        return reverse('custom_field_list')


class DeviceTypeListView(ListView):
    context_object_name = 'device_types'
    queryset = DeviceType.objects.all()
    template_name = 'device/type_list.html'


class DeviceTypeCreate(CreateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/type_create.html'

    def get_success_url(self):
        return reverse('type_list')


class DeviceTypeUpdate(UpdateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/type_update.html'

    def get_success_url(self):
        return reverse('type_list')


class DeviceTypeDelete(DeleteView):
    model = DeviceType
    template_name = 'device/type_delete.html'

    def get_success_url(self):
        return reverse('type_list')


class DeviceListView(ListView):
    context_object_name = 'devices'
    queryset = Device.objects.all()
    template_name = 'device/device_list.html'


class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_create.html'

    def get_success_url(self):
        return reverse('device_list')


class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_update.html'

    def get_success_url(self):
        return reverse('device_list')


class DeviceDelete(DeleteView):
    model = Device
    template_name = 'device/device_delete.html'

    def get_success_url(self):
        return reverse('device_list')
