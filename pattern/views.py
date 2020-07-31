from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Pattern
from .forms import PatternForm
from django.urls import reverse


@method_decorator(login_required, name='dispatch')
class PatternListView(ListView):
    context_object_name = 'patterns'
    queryset = Pattern.objects.all().order_by('id')
    template_name = 'pattern/patterns.html'


@method_decorator(login_required, name='dispatch')
class PatternCreate(CreateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'pattern/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('patterns')
        return context

    def get_success_url(self):
        return reverse('patterns')
