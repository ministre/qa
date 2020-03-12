from django.shortcuts import render
from .models import CustomField, CustomFieldItem, CustomValue, DeviceType, Vendor, Device, DevicePhoto
from .forms import CustomFieldForm, CustomFieldItemForm, DeviceTypeForm, VendorForm, DeviceForm, DevicePhotoForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class CustomFieldListView(ListView):
    context_object_name = 'custom_fields'
    queryset = CustomField.objects.all()
    template_name = 'custom_field/list.html'


@method_decorator(login_required, name='dispatch')
class CustomFieldCreate(CreateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = 'custom_field/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('custom_fields')


@method_decorator(login_required, name='dispatch')
class CustomFieldUpdate(UpdateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = 'custom_field/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('custom_field_details', kwargs={'pk': self.kwargs.get('pk')})


@method_decorator(login_required, name='dispatch')
class CustomFieldDelete(DeleteView):
    model = CustomField
    template_name = 'custom_field/delete.html'

    def get_success_url(self):
        return reverse('custom_fields')


@login_required
def custom_field_details(request, pk):
    custom_field = get_object_or_404(CustomField, id=pk)
    custom_field_items = CustomFieldItem.objects.filter(custom_field=custom_field).order_by('id')
    return render(request, 'custom_field/details.html', {'custom_field': custom_field,
                                                         'custom_field_items': custom_field_items})


@method_decorator(login_required, name='dispatch')
class CustomFieldItemCreate(CreateView):
    model = CustomFieldItem
    form_class = CustomFieldItemForm
    template_name = 'custom_field_item/create.html'

    def get_initial(self):
        return {'custom_field': self.kwargs.get('custom_field_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_field_id'] = self.kwargs.get('custom_field_id')
        return context

    def get_success_url(self):
        custom_field_update_timestamp(self.kwargs.get('custom_field_id'), self.request.user)
        return reverse('custom_field_details', kwargs={'pk': self.kwargs.get('custom_field_id')})


@method_decorator(login_required, name='dispatch')
class CustomFieldItemDelete(DeleteView):
    model = CustomFieldItem
    template_name = 'custom_field_item/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_field_id'] = self.kwargs.get('custom_field_id')
        return context

    def get_success_url(self):
        custom_field_update_timestamp(self.kwargs.get('custom_field_id'), self.request.user)
        return reverse('custom_field_details', kwargs={'pk': self.kwargs.get('custom_field_id')})


@method_decorator(login_required, name='dispatch')
class CustomFieldItemUpdate(UpdateView):
    model = CustomFieldItem
    form_class = CustomFieldItemForm
    template_name = 'custom_field_item/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_field_id'] = self.kwargs.get('custom_field_id')
        return context

    def get_success_url(self):
        custom_field_update_timestamp(self.kwargs.get('custom_field_id'), self.request.user)
        return reverse('custom_field_details', kwargs={'pk': self.kwargs.get('custom_field_id')})


def custom_field_update_timestamp(custom_field_id, user):
    custom_field = CustomField.objects.get(id=custom_field_id)
    custom_field.updated_by = user
    custom_field.updated_at = datetime.now()
    custom_field.save()
    return True


@method_decorator(login_required, name='dispatch')
class DeviceTypeListView(ListView):
    context_object_name = 'device_types'
    queryset = DeviceType.objects.all().order_by('id')
    template_name = 'type/list.html'


@method_decorator(login_required, name='dispatch')
class DeviceTypeCreate(CreateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'type/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('device_types')


@method_decorator(login_required, name='dispatch')
class DeviceTypeUpdate(UpdateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'type/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('device_types')


@method_decorator(login_required, name='dispatch')
class DeviceTypeDelete(DeleteView):
    model = DeviceType
    template_name = 'type/delete.html'

    def get_success_url(self):
        return reverse('device_types')


@method_decorator(login_required, name='dispatch')
class VendorListView(ListView):
    context_object_name = 'vendors'
    queryset = Vendor.objects.all().order_by('id')
    template_name = 'vendor/list.html'


@method_decorator(login_required, name='dispatch')
class VendorCreate(CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('vendors')


@method_decorator(login_required, name='dispatch')
class VendorUpdate(UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('vendors')


@method_decorator(login_required, name='dispatch')
class VendorDelete(DeleteView):
    model = Vendor
    template_name = 'vendor/delete.html'

    def get_success_url(self):
        return reverse('vendors')


@method_decorator(login_required, name='dispatch')
class DeviceListView(ListView):
    context_object_name = 'devices'
    queryset = Device.objects.all().order_by('id')
    template_name = 'device/list.html'


@method_decorator(login_required, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('devices')


@method_decorator(login_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('devices')


@method_decorator(login_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('devices')


def get_device_custom_values(device_id):
    custom_properties = []

    class CustomProperty:
        def __init__(self, field_id, field_name, value_name):
            self.field_id = field_id
            self.field_name = field_name
            self.value_name = value_name

    device = get_object_or_404(Device, pk=device_id)
    custom_fields = CustomField.objects.filter(custom_fields__id=device.type.id).order_by('id')
    for custom_field in custom_fields:
        try:
            custom_value = CustomValue.objects.get(Q(field=custom_field) & Q(device=device))
        except ObjectDoesNotExist:
            custom_value = ""
        custom_properties.append(CustomProperty(custom_field.id, custom_field.name, custom_value))
    return custom_properties


def set_device_custom_value(device_id, field_id, value):
    CustomValue.objects.update_or_create(device=Device.objects.get(id=device_id),
                                         field=CustomField.objects.get(id=field_id),
                                         defaults={'value': value})


@login_required
def device_details(request, pk):
    device = get_object_or_404(Device, pk=pk)
    custom_properties = get_device_custom_values(pk)
    return render(request, 'device/details.html', {'device': device, 'custom_properties': custom_properties})


@login_required
def device_update_details(request, pk):
    if request.method == 'POST':
        for item in request.POST.dict().items():
            if item[0] != 'csrfmiddlewaretoken':
                set_device_custom_value(pk, int(item[0]), item[1])
        return HttpResponseRedirect('/device/' + str(pk) + '/')
    else:
        device = get_object_or_404(Device, pk=pk)
        custom_properties = get_device_custom_values(pk)
        return render(request, 'device/device_update_details.html', {'device': device,
                                                                     'custom_properties': custom_properties})


@method_decorator(login_required, name='dispatch')
class DevicePhotoListView(ListView):
    context_object_name = 'photos'
    queryset = DevicePhoto.objects.all()
    template_name = 'device/photo_list.html'


@method_decorator(login_required, name='dispatch')
class DevicePhotoCreate(CreateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'device/photo_create.html'

    def get_success_url(self):
        return reverse('photo_list')


@method_decorator(login_required, name='dispatch')
class DevicePhotoUpdate(UpdateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'device/photo_update.html'

    def get_success_url(self):
        return reverse('photo_list')


@method_decorator(login_required, name='dispatch')
class DevicePhotoDelete(DeleteView):
    model = DevicePhoto
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('photo_list')
