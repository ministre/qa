from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import DocumType
from .forms import DocumTypeForm
from django.urls import reverse
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class TypeCreate(CreateView):
    model = DocumType
    form_class = DocumTypeForm
    template_name = 'docum/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('types')


@method_decorator(login_required, name='dispatch')
class TypeListView(ListView):
    context_object_name = 'types'
    queryset = DocumType.objects.all().order_by('id')
    template_name = 'docum/types.html'


@method_decorator(login_required, name='dispatch')
class TypeUpdate(UpdateView):
    model = DocumType
    form_class = DocumTypeForm
    template_name = 'docum/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse('types')


@method_decorator(login_required, name='dispatch')
class TypeDelete(DeleteView):
    model = DocumType
    template_name = 'docum/delete.html'

    def get_success_url(self):
        return reverse('types')
