from django.shortcuts import render
from device.models import DeviceType
from .forms import DeviceTypeForm
from django.http import HttpResponseRedirect


def device_type_list(request):
    return render(request, 'device/device_type_list.html',
                  {'device_types': DeviceType.objects.all()})


def device_type_add(request):
    if request.method == 'POST':
        form = DeviceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
    else:
        form = DeviceTypeForm()
        return render(request, 'device/device_type_add.html', {'form': form})


def device_list(request):
    return render(request, 'device/device_list.html')
