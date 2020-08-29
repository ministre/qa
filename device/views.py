from django.shortcuts import render
from .models import Vendor, DeviceChecklist, DeviceChecklistItem, DeviceChecklistItemValue, DeviceSlist, \
    DeviceSlistItem, DeviceSlistItemValue, DeviceTextField, DeviceTextFieldValue, DeviceIntegerField, \
    DeviceTypeSpecification, CustomField, CustomFieldItem, DeviceType, Device, DevicePhoto, Sample, Specification, \
    Firmware, FirmwareAccount, FirmwareFile, FirmwareScreenshot, FirmwareHowto
from docum.models import Docum
from protocol.models import Protocol
from feature.models import FeatureList
from .forms import VendorForm, DeviceChecklistForm, DeviceChecklistItemForm, DeviceSlistForm, DeviceSlistItemForm, \
    DeviceTextFieldForm, DeviceIntegerFieldForm, DeviceTypeSpecificationForm, CustomFieldForm, CustomFieldItemForm, \
    DeviceTypeForm, DeviceForm, DevicePhotoForm, SampleForm, FirmwareForm, FirmwareAccountForm, FirmwareFileForm,\
    FirmwareScreenshotForm, FirmwareHowtoForm
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

            specifications.append({'id': spec.id, 'type': spec_type, 'name': spec_name, 'unit': spec_unit,
                                   'items': spec_items, 'custom_value': custom_value})

        return specifications


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
    docums = Docum.objects.filter(device=device)
    samples = Sample.objects.filter(device=device)
    protocols = Protocol.objects.filter(device=device)
    redmine_url = settings.REDMINE_URL
    return render(request, 'device/device_details.html', {'device': device, 'specs': specs, 'fws': fws,
                                                          'photos': photos, 'docums': docums, 'samples': samples,
                                                          'protocols': protocols, 'redmine_url': redmine_url,
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
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class SampleUpdate(UpdateView):
    model = Sample
    form_class = SampleForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.kwargs.get('device_id')
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class SampleDelete(DeleteView):
    model = Sample
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_id'] = self.object.device.id
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})


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
