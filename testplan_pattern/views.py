from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Pattern
from .forms import PatternForm
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class PatternCreate(CreateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'pattern/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('patterns')


@method_decorator(login_required, name='dispatch')
class PatternListView(ListView):
    context_object_name = 'patterns'
    queryset = Pattern.objects.all().order_by('id')
    template_name = 'pattern/list.html'


@method_decorator(login_required, name='dispatch')
class PatternUpdate(UpdateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'pattern/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('patterns')


@method_decorator(login_required, name='dispatch')
class PatternDelete(DeleteView):
    model = Pattern
    template_name = 'pattern/delete.html'

    def get_success_url(self):
        return reverse('patterns')
