from django.shortcuts import render
from device.models import CustomField, CustomValue, DeviceType, Device, DevicePhoto, Button, Led
from .forms import CustomFieldForm, DeviceTypeForm, DeviceForm, DevicePhotoForm, ButtonForm, LedForm
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


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


def get_custom_properties(device_id):
    custom_properties = []

    class CustomProperty:
        def __init__(self, field, value):
            self.field = field
            self.value = value

    device = get_object_or_404(Device, pk=device_id)
    custom_fields = CustomField.objects.filter(custom_fields__id=device.type.id)
    for custom_field in custom_fields:
        try:
            custom_value = CustomValue.objects.get(Q(field=custom_field) & Q(device=device))
        except ObjectDoesNotExist:
            custom_value = ""
        custom_properties.append(CustomProperty(custom_field, custom_value))
    return custom_properties


@login_required
def device_show(request, pk):
    device = get_object_or_404(Device, pk=pk)
    custom_properties = get_custom_properties(1)
    return render(request, 'device/device_show.html', {'device': device, 'custom_properties': custom_properties})


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
