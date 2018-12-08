from django.shortcuts import render


def type_list(request):
    return render(request, 'device/type_list.html')


def device_list(request):
    return render(request, 'device/device_list.html')
