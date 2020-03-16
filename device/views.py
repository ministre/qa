from django.shortcuts import render
from .models import CustomField, CustomFieldItem, CustomValue, DeviceType, Vendor, Device, DevicePhoto
from firmware.models import Firmware
from docum.models import Docum
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
        return reverse('device_details', kwargs={'pk': self.kwargs.get('pk')})


@method_decorator(login_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('devices')


class Specification:
    def __init__(self):
        self.specs = []  # [{'name': <>, 'values': [<>, ]}]
        self.form_metadata = []
        # [{'name': <>, 'type': <>, 'id': <>, 'value': <>, 'items': [{'name': <>, 'id': <>, 'selected': <bool>}, ]}]

    def get_values(self, device: Device):
        for field in CustomField.objects.filter(custom_fields__id=device.type.id).order_by('id'):
            values = []
            for value in CustomValue.objects.filter(Q(field=field) & Q(device=device)):
                if value.item:
                    values.append(value.item)
                else:
                    values.append(value.value)
            self.specs.append({'name': field.name, 'values': values})
        return self.specs

    def get_form_metadata(self, device: Device):
        for field in CustomField.objects.filter(custom_fields__id=device.type.id).order_by('id'):
            items = []
            if field.type == 'text' or field.type == 'number':
                try:
                    value = CustomValue.objects.get(Q(field=field) & Q(device=device))
                    self.form_metadata.append({'name': field.name, 'type': field.type, 'id': field.id,
                                               'value': value.value, 'items': items})
                except ObjectDoesNotExist:
                    self.form_metadata.append({'name': field.name, 'type': field.type, 'id': field.id,
                                               'value': '', 'items': items})
            if field.type == 'listbox' or field.type == 'checkbox':
                for item in CustomFieldItem.objects.filter(custom_field=field):
                    try:
                        CustomValue.objects.get(Q(item=item) & Q(device=device))
                        items.append({'name': item.name, 'id': item.id, 'selected': True})
                    except ObjectDoesNotExist:
                        items.append({'name': item.name, 'id': item.id, 'selected': False})
                self.form_metadata.append({'name': field.name, 'type': field.type, 'id': field.id, 'value': None,
                                           'items': items})
        return self.form_metadata

    def update_value(self, device: Device, field_id: int, value: str):
        field = CustomField.objects.get(id=field_id)
        if field.type == 'text' or field.type == 'number':
            if value:
                CustomValue.objects.update_or_create(device=device, field=field, defaults={"value": value})
            else:
                CustomValue.objects.filter(Q(device=device) & Q(field=field)).delete()
            return True
        elif field.type == 'listbox':
            if value:
                CustomValue.objects.update_or_create(device=device, field=field,
                                                     defaults={"item": CustomFieldItem.objects.get(id=value)})
            else:
                CustomValue.objects.filter(Q(device=device) & Q(field=field)).delete()
        elif field.type == 'checkbox':
            pass
        return True

    def update_checkbox(self, device: Device, field_id: int, item_id: int):
        if item_id == 0:
            CustomValue.objects.filter(Q(device=device) & Q(field=CustomField.objects.get(id=field_id))).delete()
        else:
            CustomValue.objects.create(device=device, field=CustomField.objects.get(id=field_id),
                                       item=CustomFieldItem.objects.get(id=item_id))
        return True


@login_required
def device_details(request, pk):
    device = get_object_or_404(Device, pk=pk)
    fws = Firmware.objects.filter(device=device)
    docums = Docum.objects.filter(device=device)
    photos = DevicePhoto.objects.filter(device=device)
    specs = Specification().get_values(device)
    return render(request, 'device/details.html', {'device': device, 'fws': fws, 'docums': docums,
                                                   'specs': specs, 'photos': photos})


@login_required
def device_update_spec(request, pk):
    device = get_object_or_404(Device, pk=pk)
    s = Specification()
    if request.method == 'POST':
        for item in request.POST.dict().items():
            if item[0] != 'csrfmiddlewaretoken' and not item[0].startswith('checkbox_'):
                s.update_value(device, int(item[0]), item[1])
            if item[0].startswith('checkbox_'):
                checkbox_item = item[0].split('_')
                s.update_checkbox(device, int(checkbox_item[1]), int(checkbox_item[2]))
        return HttpResponseRedirect('/device/' + str(pk) + '/')
    else:
        specs = s.get_form_metadata(device)
        return render(request, 'device/update_spec.html', {'device': device, 'specs': specs})


@method_decorator(login_required, name='dispatch')
class DevicePhotoListView(ListView):
    context_object_name = 'photos'
    queryset = DevicePhoto.objects.all()
    template_name = 'device/photo_list.html'


@method_decorator(login_required, name='dispatch')
class DevicePhotoCreate(CreateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'photo/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id')})


@method_decorator(login_required, name='dispatch')
class DevicePhotoUpdate(UpdateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'photo/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id')})


@method_decorator(login_required, name='dispatch')
class DevicePhotoDelete(DeleteView):
    model = DevicePhoto
    template_name = 'photo/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id')})
