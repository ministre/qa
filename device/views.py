from django.shortcuts import render
from .models import Vendor, DeviceChecklist, DeviceChecklistItem, DeviceChecklistItemValue, DeviceSlist, \
    DeviceSlistItem, DeviceSlistItemValue, DeviceTextField, DeviceTextFieldValue, DeviceIntegerField, \
    DeviceIntegerFieldValue, DeviceTypeSpecification, DeviceType, Device, DeviceDocumentType, DeviceDocument, \
    DevicePhoto, DeviceSample, DeviceSupport, Firmware, FirmwareAccount, FirmwareFile, FirmwareScreenshot, \
    FirmwareHowto
from protocol.models import ProtocolDevice
from feature.models import FeatureList
from contact.models import Contact
from .forms import VendorForm, DeviceChecklistForm, DeviceChecklistItemForm, DeviceSlistForm, DeviceSlistItemForm, \
    DeviceTextFieldForm, DeviceIntegerFieldForm, DeviceTypeSpecificationForm, DeviceTypeForm, DeviceForm, \
    DeviceDocumentTypeForm, DeviceDocumentForm, DevicePhotoForm, DeviceSampleForm, DeviceSupportForm, FirmwareForm, \
    FirmwareAccountForm, FirmwareFileForm, FirmwareScreenshotForm, FirmwareHowtoForm
from redmine.forms import ExportDeviceTypeForm, ImportDeviceTypeForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from datetime import datetime
from django import forms
from qa import settings


class Item(object):
    @staticmethod
    def update_timestamp(foo, user):
        foo.updated_by = user
        foo.updated_at = datetime.now()
        foo.save()


class Spec(object):
    @staticmethod
    def get_values(device: Device):
        specs = DeviceTypeSpecification.objects.filter(type=device.type).order_by('id')
        specifications = []
        for spec in specs:
            spec_type = spec.get_type()
            spec_name = None
            spec_unit = None
            custom_value = None
            spec_items = []
            if spec_type == 'checklist':
                spec_name = spec.checklist.name

                items = DeviceChecklistItem.objects.filter(checklist=spec.checklist).order_by('id')
                for item in items:
                    value = False
                    item_values = DeviceChecklistItemValue.objects.filter(device=device, item=item)
                    for item_value in item_values:
                        value = item_value.value

                    spec_items.append({'id': item.id, 'name': item.name, 'value': value})

            if spec_type == 'slist':
                spec_name = spec.slist.name

                items = DeviceSlistItem.objects.filter(slist=spec.slist).order_by('id')
                for item in items:
                    value = False
                    item_values = DeviceSlistItemValue.objects.filter(device=device, value=item)
                    for item_value in item_values:
                        value = item_value.value

                    spec_items.append({'id': item.id, 'name': item.name, 'value': value})

            if spec_type == 'text_field':
                spec_name = spec.text_field.name
                item_values = DeviceTextFieldValue.objects.filter(device=device, field=spec.text_field)
                for item_value in item_values:
                    custom_value = item_value.value

            if spec_type == 'integer_field':
                spec_name = spec.integer_field.name
                spec_unit = spec.integer_field.unit
                item_values = DeviceIntegerFieldValue.objects.filter(device=device, field=spec.integer_field)
                for item_value in item_values:
                    custom_value = item_value.value

            specifications.append({'id': spec.id, 'type': spec_type, 'name': spec_name, 'unit': spec_unit,
                                   'items': spec_items, 'custom_value': custom_value})

        return specifications

    @staticmethod
    def set_values(device: Device, dt_spec: DeviceTypeSpecification, values):
        if dt_spec.checklist:
            items = DeviceChecklistItem.objects.filter(checklist=dt_spec.checklist)
            for item in items:
                DeviceChecklistItemValue.objects.filter(device=device, item=item).delete()
            for value in values:
                item = DeviceChecklistItem.objects.get(checklist=dt_spec.checklist, id=value)
                DeviceChecklistItemValue.objects.create(device=device, item=item, value=True)

        if dt_spec.slist:
            items = DeviceSlistItem.objects.filter(slist=dt_spec.slist)
            for item in items:
                DeviceSlistItemValue.objects.filter(device=device, value=item).delete()
            if values[0]:
                item = DeviceSlistItem.objects.get(slist=dt_spec.slist, id=values[0])
                DeviceSlistItemValue.objects.create(device=device, value=item)

        if dt_spec.text_field:
            if values[0]:
                DeviceTextFieldValue.objects.update_or_create(device=device, field=dt_spec.text_field,
                                                              defaults={'value': values[0]})
            else:
                DeviceTextFieldValue.objects.filter(device=device, field=dt_spec.text_field).delete()

        if dt_spec.integer_field:
            if values[0]:
                DeviceIntegerFieldValue.objects.update_or_create(device=device, field=dt_spec.integer_field,
                                                                 defaults={'value': values[0]})
            else:
                DeviceIntegerFieldValue.objects.filter(device=device, field=dt_spec.integer_field).delete()


@login_required
def spec_update(request):
    if request.method == 'POST':
        device = get_object_or_404(Device, id=request.POST['device_id'])
        dt_spec = get_object_or_404(DeviceTypeSpecification, id=request.POST['spec_id'])

        values = []
        if dt_spec.checklist:
            for item in request.POST.dict().items():
                if item[0].startswith('item_'):
                    values.append(item[0][5:])
        else:
            values.append(request.POST['spec_value'])

        Spec.set_values(device=device, dt_spec=dt_spec, values=values)
        return HttpResponseRedirect(reverse('device_details', kwargs={'pk': device.id, 'tab_id': 2}))
    else:
        return HttpResponseRedirect(reverse('devices'))


@method_decorator(login_required, name='dispatch')
class VendorListView(ListView):
    context_object_name = 'vendors'
    queryset = Vendor.objects.all().order_by('name')
    template_name = 'device/vendors.html'


@method_decorator(login_required, name='dispatch')
class VendorCreate(CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('vendors')
        return context

    def get_success_url(self):
        return reverse('vendors')


@method_decorator(login_required, name='dispatch')
class VendorUpdate(UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('vendor_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('vendor_details', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class VendorDelete(DeleteView):
    model = Vendor
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('vendor_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('vendors')


@login_required
def vendor_details(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    return render(request, 'device/vendor_details.html', {'vendor': vendor})


@method_decorator(login_required, name='dispatch')
class DeviceChecklistListView(ListView):
    context_object_name = 'checklists'
    queryset = DeviceChecklist.objects.all().order_by('id')
    template_name = 'device/checklists.html'


@method_decorator(login_required, name='dispatch')
class DeviceChecklistCreate(CreateView):
    model = DeviceChecklist
    form_class = DeviceChecklistForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_checklists')
        return context

    def get_success_url(self):
        return reverse('d_checklists')


@method_decorator(login_required, name='dispatch')
class DeviceChecklistUpdate(UpdateView):
    model = DeviceChecklist
    form_class = DeviceChecklistForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_checklist_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('d_checklist_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceChecklistDelete(DeleteView):
    model = DeviceChecklist
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_checklist_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('d_checklists')


@login_required
def device_checklist_details(request, pk, tab_id):
    checklist = get_object_or_404(DeviceChecklist, id=pk)
    return render(request, 'device/checklist_details.html', {'tab_id': tab_id, 'checklist': checklist})


@method_decorator(login_required, name='dispatch')
class DeviceChecklistItemCreate(CreateView):
    model = DeviceChecklistItem
    form_class = DeviceChecklistItemForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'checklist': self.kwargs.get('cl_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklist = get_object_or_404(DeviceChecklist, id=self.kwargs.get('cl_id'))
        context['back_url'] = reverse('d_checklist_details', kwargs={'pk': checklist.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.checklist, user=self.request.user)
        return reverse('d_checklist_details', kwargs={'pk': self.object.checklist.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class DeviceChecklistItemUpdate(UpdateView):
    model = DeviceChecklistItem
    form_class = DeviceChecklistItemForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'checklist_id': self.kwargs.get('cl_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_checklist_details', kwargs={'pk': self.object.checklist.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.checklist, user=self.request.user)
        return reverse('d_checklist_details', kwargs={'pk': self.object.checklist.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class DeviceChecklistItemDelete(DeleteView):
    model = DeviceChecklistItem
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_checklist_details', kwargs={'pk': self.object.checklist.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.checklist, user=self.request.user)
        return reverse('d_checklist_details', kwargs={'pk': self.object.checklist.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class DeviceSlistListView(ListView):
    context_object_name = 'slists'
    queryset = DeviceSlist.objects.all().order_by('id')
    template_name = 'device/slists.html'


@method_decorator(login_required, name='dispatch')
class DeviceSlistCreate(CreateView):
    model = DeviceSlist
    form_class = DeviceSlistForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_slists')
        return context

    def get_success_url(self):
        return reverse('d_slists')


@method_decorator(login_required, name='dispatch')
class DeviceSlistUpdate(UpdateView):
    model = DeviceSlist
    form_class = DeviceSlistForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_slist_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('d_slist_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceSlistDelete(DeleteView):
    model = DeviceSlist
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_slist_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('d_slists')


@login_required
def device_slist_details(request, pk, tab_id):
    slist = get_object_or_404(DeviceSlist, id=pk)
    return render(request, 'device/slist_details.html', {'tab_id': tab_id, 'slist': slist})


@method_decorator(login_required, name='dispatch')
class DeviceSlistItemCreate(CreateView):
    model = DeviceSlistItem
    form_class = DeviceSlistItemForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'slist': self.kwargs.get('sl_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slist = get_object_or_404(DeviceSlist, id=self.kwargs.get('sl_id'))
        context['back_url'] = reverse('d_slist_details', kwargs={'pk': slist.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.slist, user=self.request.user)
        return reverse('d_slist_details', kwargs={'pk': self.object.slist.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class DeviceSlistItemUpdate(UpdateView):
    model = DeviceSlistItem
    form_class = DeviceSlistItemForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'slist_id': self.kwargs.get('sl_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_slist_details', kwargs={'pk': self.object.slist.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.slist, user=self.request.user)
        return reverse('d_slist_details', kwargs={'pk': self.object.slist.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class DeviceSlistItemDelete(DeleteView):
    model = DeviceSlistItem
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_slist_details', kwargs={'pk': self.object.slist.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.slist, user=self.request.user)
        return reverse('d_slist_details', kwargs={'pk': self.object.slist.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class DeviceTextFieldListView(ListView):
    context_object_name = 'tfields'
    queryset = DeviceTextField.objects.all().order_by('id')
    template_name = 'device/tfields.html'


@method_decorator(login_required, name='dispatch')
class DeviceTextFieldCreate(CreateView):
    model = DeviceTextField
    form_class = DeviceTextFieldForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_tfields')
        return context

    def get_success_url(self):
        return reverse('d_tfields')


@method_decorator(login_required, name='dispatch')
class DeviceTextFieldUpdate(UpdateView):
    model = DeviceTextField
    form_class = DeviceTextFieldForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_tf_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('d_tf_details', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class DeviceTextFieldDelete(DeleteView):
    model = DeviceTextField
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_tf_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('d_tfields')


@login_required
def device_tf_details(request, pk):
    tfield = get_object_or_404(DeviceTextField, id=pk)
    return render(request, 'device/tfield_details.html', {'tfield': tfield})


@method_decorator(login_required, name='dispatch')
class DeviceIntegerFieldListView(ListView):
    context_object_name = 'ifields'
    queryset = DeviceIntegerField.objects.all().order_by('id')
    template_name = 'device/ifields.html'


@method_decorator(login_required, name='dispatch')
class DeviceIntegerFieldCreate(CreateView):
    model = DeviceIntegerField
    form_class = DeviceIntegerFieldForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_ifields')
        return context

    def get_success_url(self):
        return reverse('d_ifields')


@method_decorator(login_required, name='dispatch')
class DeviceIntegerFieldUpdate(UpdateView):
    model = DeviceIntegerField
    form_class = DeviceIntegerFieldForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_if_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('d_if_details', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class DeviceIntegerFieldDelete(DeleteView):
    model = DeviceIntegerField
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_if_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('d_ifields')


@login_required
def device_if_details(request, pk):
    ifield = get_object_or_404(DeviceIntegerField, id=pk)
    return render(request, 'device/ifield_details.html', {'ifield': ifield})


@method_decorator(login_required, name='dispatch')
class DeviceTypeListView(ListView):
    context_object_name = 'device_types'
    queryset = DeviceType.objects.all().order_by('id')
    template_name = 'device/types.html'


@method_decorator(login_required, name='dispatch')
class DeviceTypeCreate(CreateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_types')
        return context

    def get_success_url(self):
        return reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceTypeUpdate(UpdateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceTypeDelete(DeleteView):
    model = DeviceType
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('device_types')


@login_required
def device_type_details(request, pk, tab_id):
    device_type = get_object_or_404(DeviceType, pk=pk)
    devices_count = device_type.devices_count()
    testplans_count = device_type.testplans_count()
    specs = DeviceTypeSpecification.objects.filter(type=device_type).order_by('id')
    feature_lists = FeatureList.objects.filter(device_type=device_type).order_by('id')
    redmine_url = settings.REDMINE_URL
    export_form = ExportDeviceTypeForm(initial={'parent': device_type.redmine_parent,
                                                'project': device_type.redmine_project,
                                                'project_name': device_type.redmine_project_name,
                                                'specs': True,
                                                'tech_reqs': True})
    import_form = ImportDeviceTypeForm(initial={'project': device_type.redmine_project})
    return render(request, 'device/type_details.html', {'device_type': device_type,
                                                        'devices_count': devices_count,
                                                        'testplans_count': testplans_count,
                                                        'specs': specs,
                                                        'feature_lists': feature_lists,
                                                        'redmine_url': redmine_url,
                                                        'export_form': export_form,
                                                        'import_form': import_form,
                                                        'tab_id': tab_id})


@login_required
def dt_spec_create(request, dt: int, st: int):
    if request.method == 'POST':
        form = DeviceTypeSpecificationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('device_type_details', kwargs={'pk': dt, 'tab_id': 2}))
    else:
        device_type = get_object_or_404(DeviceType, id=dt)
        form = DeviceTypeSpecificationForm(initial={'type': device_type})
        if st == 1:
            form.fields['checklist'].required = True
            form.fields['slist'].widget = forms.HiddenInput()
            form.fields['text_field'].widget = forms.HiddenInput()
            form.fields['integer_field'].widget = forms.HiddenInput()
        elif st == 2:
            form.fields['checklist'].widget = forms.HiddenInput()
            form.fields['slist'].required = True
            form.fields['text_field'].widget = forms.HiddenInput()
            form.fields['integer_field'].widget = forms.HiddenInput()
        elif st == 3:
            form.fields['checklist'].widget = forms.HiddenInput()
            form.fields['slist'].widget = forms.HiddenInput()
            form.fields['text_field'].required = True
            form.fields['integer_field'].widget = forms.HiddenInput()
        elif st == 4:
            form.fields['checklist'].widget = forms.HiddenInput()
            form.fields['slist'].widget = forms.HiddenInput()
            form.fields['text_field'].widget = forms.HiddenInput()
            form.fields['integer_field'].required = True
        back_url = reverse('device_type_details', kwargs={'pk': device_type.id, 'tab_id': 2})
        return render(request, 'device/create.html', {'form': form, 'back_url': back_url})


@login_required
def dt_spec_delete(request, dt: int, pk: int):
    if request.method == 'POST':
        DeviceTypeSpecification.objects.filter(id=pk).delete()
        return HttpResponseRedirect(reverse('device_type_details', kwargs={'pk': dt, 'tab_id': 2}))
    else:
        spec = get_object_or_404(DeviceTypeSpecification, id=pk)
        back_url = reverse('device_type_details', kwargs={'pk': spec.type.id, 'tab_id': 2})
        return render(request, 'device/delete.html', {'object': spec, 'back_url': back_url})


@method_decorator(login_required, name='dispatch')
class DeviceListView(ListView):
    context_object_name = 'devices'
    queryset = Device.objects.all().order_by('id')
    template_name = 'device/device_list.html'


@method_decorator(login_required, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('devices')
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('devices')


@login_required
def device_details(request, pk, tab_id):
    device = get_object_or_404(Device, pk=pk)
    specs = Spec.get_values(device)
    fws = Firmware.objects.filter(device=device)
    photos = DevicePhoto.objects.filter(device=device)
    docs = DeviceDocument.objects.filter(device=device).order_by('id')
    samples = DeviceSample.objects.filter(device=device).order_by('id')
    protocol_devices = ProtocolDevice.objects.filter(device=device).order_by('id')
    supports = DeviceSupport.objects.filter(device=device).order_by('id')
    redmine_url = settings.REDMINE_URL
    return render(request, 'device/device_details.html', {'device': device, 'specs': specs, 'fws': fws,
                                                          'photos': photos, 'docs': docs, 'samples': samples,
                                                          'protocol_devices': protocol_devices, 'supports': supports,
                                                          'redmine_url': redmine_url,
                                                          'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class DeviceDocumentTypeListView(ListView):
    context_object_name = 'doc_types'
    queryset = DeviceDocumentType.objects.all().order_by('id')
    template_name = 'device/doc_types.html'


@method_decorator(login_required, name='dispatch')
class DeviceDocumentTypeCreate(CreateView):
    model = DeviceDocumentType
    form_class = DeviceDocumentTypeForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_doc_types')
        return context

    def get_success_url(self):
        return reverse('d_doc_types')


@method_decorator(login_required, name='dispatch')
class DeviceDocumentTypeUpdate(UpdateView):
    model = DeviceDocumentType
    form_class = DeviceDocumentTypeForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_doc_types')
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        return reverse('d_doc_types')


@method_decorator(login_required, name='dispatch')
class DeviceDocumentTypeDelete(DeleteView):
    model = DeviceDocumentType
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('d_doc_types')
        return context

    def get_success_url(self):
        return reverse('d_doc_types')


@method_decorator(login_required, name='dispatch')
class DevicePhotoListView(ListView):
    context_object_name = 'photos'
    queryset = DevicePhoto.objects.all()
    template_name = 'device/photo_list.html'


@method_decorator(login_required, name='dispatch')
class DevicePhotoCreate(CreateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('d_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DevicePhotoUpdate(UpdateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DevicePhotoDelete(DeleteView):
    model = DevicePhoto
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DeviceDocumentCreate(CreateView):
    model = DeviceDocument
    form_class = DeviceDocumentForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('d_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class DeviceDocumentUpdate(UpdateView):
    model = DeviceDocument
    form_class = DeviceDocumentForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class DeviceDocumentDelete(DeleteView):
    model = DeviceDocument
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class DeviceSampleCreate(CreateView):
    model = DeviceSample
    form_class = DeviceSampleForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('d_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class DeviceSampleUpdate(UpdateView):
    model = DeviceSample
    form_class = DeviceSampleForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class DeviceSampleDelete(DeleteView):
    model = DeviceSample
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class FirmwareCreate(CreateView):
    model = Firmware
    form_class = FirmwareForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('d_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 3})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class FirmwareUpdate(UpdateView):
    model = Firmware
    form_class = FirmwareForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class FirmwareDelete(DeleteView):
    model = Firmware
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 3})


@login_required
def fw_details(request, pk, tab_id: int):
    fw = get_object_or_404(Firmware, id=pk)
    fw_accounts = FirmwareAccount.objects.filter(firmware=fw).order_by('id')
    fw_hts = FirmwareHowto.objects.filter(firmware=fw).order_by('id')
    fw_files = FirmwareFile.objects.filter(firmware=fw).order_by('id')
    fw_screenshots = FirmwareScreenshot.objects.filter(firmware=fw).order_by('id')
    return render(request, 'device/fw_details.html', {'fw': fw, 'fw_accounts': fw_accounts, 'fw_hts': fw_hts,
                                                      'fw_files': fw_files, 'fw_screenshots': fw_screenshots,
                                                      'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class FirmwareAccountCreate(CreateView):
    model = FirmwareAccount
    form_class = FirmwareAccountForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'firmware': self.kwargs.get('fw_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class FirmwareAccountUpdate(UpdateView):
    model = FirmwareAccount
    form_class = FirmwareAccountForm
    template_name = 'device/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class FirmwareAccountDelete(DeleteView):
    model = FirmwareAccount
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class FirmwareFileCreate(CreateView):
    model = FirmwareFile
    form_class = FirmwareFileForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'firmware': self.kwargs.get('fw_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class FirmwareFileUpdate(UpdateView):
    model = FirmwareFile
    form_class = FirmwareFileForm
    template_name = 'device/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class FirmwareFileDelete(DeleteView):
    model = FirmwareFile
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class FirmwareScreenshotCreate(CreateView):
    model = FirmwareScreenshot
    form_class = FirmwareScreenshotForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'firmware': self.kwargs.get('fw_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class FirmwareScreenshotUpdate(UpdateView):
    model = FirmwareScreenshot
    form_class = FirmwareScreenshotForm
    template_name = 'device/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class FirmwareScreenshotDelete(DeleteView):
    model = FirmwareScreenshot
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class FirmwareHowtoCreate(CreateView):
    model = FirmwareHowto
    form_class = FirmwareHowtoForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'firmware': self.kwargs.get('fw_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 7})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.kwargs.get('fw_id'), 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class FirmwareHowtoUpdate(UpdateView):
    model = FirmwareHowto
    form_class = FirmwareHowtoForm
    template_name = 'device/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class FirmwareHowtoDelete(DeleteView):
    model = FirmwareHowto
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        return reverse('fw_details', kwargs={'pk': self.object.firmware.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class DeviceSupportCreate(CreateView):
    model = DeviceSupport
    form_class = DeviceSupportForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('d_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_form(self, form_class=DeviceSupportForm):
        form = super(DeviceSupportCreate, self).get_form(form_class)
        form.fields['contact'].queryset = Contact.objects.exclude(vendor__isnull=True).order_by('surname')
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 8})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('d_id'), 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class DeviceSupportDelete(DeleteView):
    model = DeviceSupport
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 8})
