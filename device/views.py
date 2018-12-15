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


def device_type_edit(request, device_type_id):
    if request.method == 'POST':
        form = DeviceTypeForm(request.POST)
        if form.is_valid():
            device_type = DeviceType.objects.get(id=device_type_id)
            device_type.tag = request.POST['tag']
            device_type.desc = request.POST['desc']
            device_type.save()
            return HttpResponseRedirect('..')
    else:
        device_type = DeviceType.objects.get(id=device_type_id)
        form = DeviceTypeForm(initial={'tag': device_type.tag, 'desc': device_type.desc})
        return render(request, 'device/device_type_edit.html', {'form': form, 'device_type': device_type})


def device_list(request):
    return render(request, 'device/device_list.html')
