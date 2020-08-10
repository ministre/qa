from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse
from datetime import datetime
#from .models import Firmware
#from .forms import FirmwareForm


#@method_decorator(login_required, name='dispatch')
#class FirmwareCreate(CreateView):
#    model = Firmware
#    form_class = FirmwareForm
#    template_name = 'firmware/create.html'
#
#    def get_initial(self):
#        return {'device': self.kwargs.get('device_id'),
#                'created_by': self.request.user, 'updated_by': self.request.user}
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['device_id'] = self.kwargs.get('device_id')
#        return context
#
#    def get_success_url(self):
#        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 3})


#@method_decorator(login_required, name='dispatch')
#class FirmwareUpdate(UpdateView):
#    model = Firmware
#    form_class = FirmwareForm
#    template_name = 'firmware/update.html'
#
#    def get_initial(self):
#        return {'updated_by': self.request.user, 'updated_at': datetime.now}
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['device_id'] = self.kwargs.get('device_id')
#        return context

#    def get_success_url(self):
#        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id')})


#@method_decorator(login_required, name='dispatch')
#class FirmwareDelete(DeleteView):
#    model = Firmware
#    template_name = 'firmware/delete.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['device_id'] = self.kwargs.get('device_id')
#        return context

#    def get_success_url(self):
#        return reverse('device_details', kwargs={'pk': self.kwargs.get('device_id')})
