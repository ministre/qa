from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import DocumType, Docum
from .forms import DocumTypeForm, DocumForm
from django.urls import reverse
from datetime import datetime


# document types
@method_decorator(login_required, name='dispatch')
class TypeCreate(CreateView):
    model = DocumType
    form_class = DocumTypeForm
    template_name = 'docum_type/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('docum_types')


@method_decorator(login_required, name='dispatch')
class TypeListView(ListView):
    context_object_name = 'types'
    queryset = DocumType.objects.all().order_by('id')
    template_name = 'docum_type/list.html'


@method_decorator(login_required, name='dispatch')
class TypeUpdate(UpdateView):
    model = DocumType
    form_class = DocumTypeForm
    template_name = 'docum_type/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('docum_types')


@method_decorator(login_required, name='dispatch')
class TypeDelete(DeleteView):
    model = DocumType
    template_name = 'docum_type/delete.html'

    def get_success_url(self):
        return reverse('docum_types')


# documents
@method_decorator(login_required, name='dispatch')
class DocumCreate(CreateView):
    model = Docum
    form_class = DocumForm
    template_name = 'docum/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('docums')


@method_decorator(login_required, name='dispatch')
class DocumListView(ListView):
    context_object_name = 'docums'
    queryset = Docum.objects.all().order_by('id')
    template_name = 'docum/list.html'


@method_decorator(login_required, name='dispatch')
class DocumUpdate(UpdateView):
    model = Docum
    form_class = DocumForm
    template_name = 'docum/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('docums')


@method_decorator(login_required, name='dispatch')
class DocumDelete(DeleteView):
    model = Docum
    template_name = 'docum/delete.html'

    def get_success_url(self):
        return reverse('docums')
