from django.shortcuts import render
from .models import CustomField, CustomFieldItem, DeviceType, Vendor, Device, DevicePhoto, Sample, Specification
from firmware.models import Firmware
from docum.models import Docum
from protocol.models import Protocol
from .forms import CustomFieldForm, CustomFieldItemForm, DeviceTypeForm, VendorForm, DeviceForm, DevicePhotoForm, \
    SampleForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from datetime import datetime
from redmine.models import RedmineProject


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
    return render(request, 'custom_field_item/list.html', {'custom_field': custom_field,
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
        return reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceTypeUpdate(UpdateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'type/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})


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
        return reverse('device_update_spec', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('pk'), 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('devices')


@login_required
def device_type_details(request, pk, tab_id):
    device_type = get_object_or_404(DeviceType, pk=pk)
    devices_count = device_type.devices_count()
    r = RedmineProject(device_type.redmine_project)
    return render(request, 'type/details.html', {'device_type': device_type,
                                                 'redmine_wiki': r.get_wiki_url('wiki'),
                                                 'devices_count': devices_count,
                                                 'tab_id': tab_id})


@login_required
def device_details(request, pk, tab_id):
    device = get_object_or_404(Device, pk=pk)
    specs = Specification().get_values(device)
    fws = Firmware.objects.filter(device=device)
    photos = DevicePhoto.objects.filter(device=device)
    docums = Docum.objects.filter(device=device)
    samples = Sample.objects.filter(device=device)
    protocols = Protocol.objects.filter(device=device)
    r = RedmineProject(device.redmine_project)
    return render(request, 'device/details.html', {'device': device, 'specs': specs, 'fws': fws,
                                                   'photos': photos, 'docums': docums, 'samples': samples,
                                                   'protocols': protocols, 'redmine_wiki': r.get_wiki_url('wiki'),
                                                   'tab_id': tab_id})


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
        return HttpResponseRedirect(reverse('device_details', kwargs={'pk': pk, 'tab_id': 2}))
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
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 4})


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
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DevicePhotoDelete(DeleteView):
    model = DevicePhoto
    template_name = 'photo/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class SampleCreate(CreateView):
    model = Sample
    form_class = SampleForm
    template_name = 'sample/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class SampleUpdate(UpdateView):
    model = Sample
    form_class = SampleForm
    template_name = 'sample/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class SampleDelete(DeleteView):
    model = Sample
    template_name = 'sample/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})
