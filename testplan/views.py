from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from testplan.models import TestplanPattern
from .forms import TestplanPatternForm


@method_decorator(login_required, name='dispatch')
class TestplanPatternListView(ListView):
    context_object_name = 'testplan_patterns'
    queryset = TestplanPattern.objects.all()
    template_name = 'testplan/testplan_pattern_list.html'


@method_decorator(login_required, name='dispatch')
class TestplanPatternCreate(CreateView):
    model = TestplanPattern
    form_class = TestplanPatternForm
    template_name = 'testplan/create.html'

    def get_success_url(self):
        return reverse('testplan_pattern_list')


@method_decorator(login_required, name='dispatch')
class TestplanPatternUpdate(UpdateView):
    model = TestplanPattern
    form_class = TestplanPatternForm
    template_name = 'testplan/update.html'

    def get_success_url(self):
        return reverse('testplan_pattern_list')


@method_decorator(login_required, name='dispatch')
class TestplanPatternDelete(DeleteView):
    model = TestplanPattern
    template_name = 'testplan/delete.html'

    def get_success_url(self):
        return reverse('testplan_pattern_list')
