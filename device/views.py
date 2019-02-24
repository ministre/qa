from django.shortcuts import render
from device.models import CustomField, CustomValue, DeviceType, Device, DevicePhoto, Button, Led, Firmware, \
    Interface, DeviceInterface
from .forms import CustomFieldForm, DeviceTypeForm, DeviceForm, DevicePhotoForm, ButtonForm, LedForm, FirmwareForm, \
    InterfaceForm
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect


@method_decorator(login_required, name='dispatch')
class InterfaceListView(ListView):
    context_object_name = 'interfaces'
    queryset = Interface.objects.all()
    template_name = 'device/interface_list.html'


@method_decorator(login_required, name='dispatch')
class InterfaceCreate(CreateView):
    model = Interface
    form_class = InterfaceForm
    template_name = 'device/interface_create.html'

    def get_success_url(self):
        return reverse('interface_list')


@method_decorator(login_required, name='dispatch')
class InterfaceUpdate(UpdateView):
    model = Interface
    form_class = InterfaceForm
    template_name = 'device/interface_update.html'

    def get_success_url(self):
        return reverse('interface_list')


@method_decorator(login_required, name='dispatch')
class InterfaceDelete(DeleteView):
    model = Interface
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('interface_list')


@method_decorator(login_required, name='dispatch')
class CustomFieldListView(ListView):
    context_object_name = 'custom_fields'
    queryset = CustomField.objects.all()
    template_name = 'device/custom_field_list.html'


@method_decorator(login_required, name='dispatch')
class CustomFieldCreate(CreateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = 'device/custom_field_create.html'

    def get_success_url(self):
        return reverse('custom_field_list')


@method_decorator(login_required, name='dispatch')
class CustomFieldUpdate(UpdateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = 'device/custom_field_update.html'

    def get_success_url(self):
        return reverse('custom_field_list')


@method_decorator(login_required, name='dispatch')
class CustomFieldDelete(DeleteView):
    model = CustomField
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('custom_field_list')


@method_decorator(login_required, name='dispatch')
class DeviceTypeListView(ListView):
    context_object_name = 'device_types'
    queryset = DeviceType.objects.all()
    template_name = 'device/type_list.html'


@method_decorator(login_required, name='dispatch')
class DeviceTypeCreate(CreateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/type_create.html'

    def get_success_url(self):
        return reverse('type_list')


@method_decorator(login_required, name='dispatch')
class DeviceTypeUpdate(UpdateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/type_update.html'

    def get_success_url(self):
        return reverse('type_list')


@method_decorator(login_required, name='dispatch')
class DeviceTypeDelete(DeleteView):
    model = DeviceType
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('type_list')


@method_decorator(login_required, name='dispatch')
class DeviceListView(ListView):
    context_object_name = 'devices'
    queryset = Device.objects.all()
    template_name = 'device/device_list.html'


@method_decorator(login_required, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_create.html'

    def get_initial(self):
        return {'created_by': self.request.user}

    def get_success_url(self):
        return reverse('device_list')


@method_decorator(login_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/device_update.html'

    def get_success_url(self):
        return reverse('device_list')


@method_decorator(login_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('device_list')


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


def get_device_interfaces(device_id):
    device_interfaces = []

    class DeviceIface:
        def __init__(self, iface_id, iface_name, iface_quantity):
            self.iface_id = iface_id
            self.iface_name = iface_name
            self.iface_quantity = iface_quantity

    device = get_object_or_404(Device, pk=device_id)
    interfaces = Interface.objects.filter(interfaces__id=device.type.id).order_by('id')
    for interface in interfaces:
        try:
            quantity = DeviceInterface.objects.get(Q(interface=interface) & Q(device=device)).quantity
        except ObjectDoesNotExist:
            quantity = 0
        device_interfaces.append(DeviceIface(interface.id, interface.name, quantity))
    return device_interfaces


def set_device_interface(device_id, iface_id, quantity):
    DeviceInterface.objects.update_or_create(device=Device.objects.get(id=device_id),
                                             interface=Interface.objects.get(id=iface_id),
                                             defaults={'quantity': quantity})


@login_required
def device_show(request, pk):
    device = get_object_or_404(Device, pk=pk)
    custom_properties = get_device_custom_values(pk)
    interfaces = get_device_interfaces(pk)
    return render(request, 'device/device_show.html', {'device': device, 'custom_properties': custom_properties,
                                                       'interfaces': interfaces})


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


@login_required
def device_update_interfaces(request, pk):
    if request.method == 'POST':
        for item in request.POST.dict().items():
            if item[0] != 'csrfmiddlewaretoken':
                set_device_interface(pk, int(item[0]), item[1])
        return HttpResponseRedirect('/device/' + str(pk) + '/')
    else:
        device = get_object_or_404(Device, pk=pk)
        interfaces = get_device_interfaces(pk)
        return render(request, 'device/device_update_interfaces.html', {'device': device,
                                                                        'interfaces': interfaces})


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


@method_decorator(login_required, name='dispatch')
class ButtonListView(ListView):
    context_object_name = 'buttons'
    queryset = Button.objects.all()
    template_name = 'device/button_list.html'


@method_decorator(login_required, name='dispatch')
class ButtonCreate(CreateView):
    model = Button
    form_class = ButtonForm
    template_name = 'device/button_create.html'

    def get_success_url(self):
        return reverse('button_list')


@method_decorator(login_required, name='dispatch')
class ButtonUpdate(UpdateView):
    model = Button
    form_class = ButtonForm
    template_name = 'device/button_update.html'

    def get_success_url(self):
        return reverse('button_list')


@method_decorator(login_required, name='dispatch')
class ButtonDelete(DeleteView):
    model = Button
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('button_list')


@method_decorator(login_required, name='dispatch')
class LedListView(ListView):
    context_object_name = 'leds'
    queryset = Led.objects.all()
    template_name = 'device/led_list.html'


@method_decorator(login_required, name='dispatch')
class LedCreate(CreateView):
    model = Led
    form_class = LedForm
    template_name = 'device/led_create.html'

    def get_success_url(self):
        return reverse('led_list')


@method_decorator(login_required, name='dispatch')
class LedUpdate(UpdateView):
    model = Led
    form_class = LedForm
    template_name = 'device/led_update.html'

    def get_success_url(self):
        return reverse('led_list')


@method_decorator(login_required, name='dispatch')
class LedDelete(DeleteView):
    model = Led
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('led_list')


@method_decorator(login_required, name='dispatch')
class FirmwareListView(ListView):
    context_object_name = 'firmwares'
    queryset = Firmware.objects.all()
    template_name = 'device/firmware_list.html'


@method_decorator(login_required, name='dispatch')
class FirmwareCreate(CreateView):
    model = Firmware
    form_class = FirmwareForm
    template_name = 'device/firmware_create.html'

    def get_initial(self):
        return {'created_by': self.request.user}

    def get_success_url(self):
        return reverse('firmware_list')


@method_decorator(login_required, name='dispatch')
class FirmwareUpdate(UpdateView):
    model = Firmware
    form_class = FirmwareForm
    template_name = 'device/firmware_update.html'

    def get_success_url(self):
        return reverse('firmware_list')


@method_decorator(login_required, name='dispatch')
class FirmwareDelete(DeleteView):
    model = Firmware
    template_name = 'device/delete.html'

    def get_success_url(self):
        return reverse('firmware_list')
