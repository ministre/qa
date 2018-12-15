from django.shortcuts import render, get_object_or_404, redirect
from device.models import DeviceType
from .forms import DeviceTypeForm


def device_type_list(request):
    return render(request, 'device/device_type_list.html',
                  {'device_types': DeviceType.objects.all()})


def device_type_add(request):
    if request.method == 'POST':
        form = DeviceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_type_list')
    else:
        form = DeviceTypeForm()
        return render(request, 'device/device_type_add.html', {'form': form})


def device_type_edit(request, pk):
    instance = get_object_or_404(DeviceType, pk=pk)
    form = DeviceTypeForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('device_type_list')
    return render(request, 'device/device_type_edit.html', {'form': form})


def device_type_delete(request, pk):
    DeviceType.objects.get(pk=pk).delete()
    return redirect('device_type_list')


def device_list(request):
    return render(request, 'device/device_list.html')
