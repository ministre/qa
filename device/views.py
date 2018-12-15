from django.shortcuts import render
from device.models import DeviceType


def device_type_list(request):
    return render(request, 'device/device_type_list.html',
                  {'device_types': DeviceType.objects.all()})


def device_list(request):
    return render(request, 'device/device_list.html')
