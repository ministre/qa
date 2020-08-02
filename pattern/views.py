from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Pattern, PatternCategory
from .forms import PatternForm, PatternCategoryForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime


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


@method_decorator(login_required, name='dispatch')
class PatternUpdate(UpdateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'pattern/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        self.object.update_timestamp(user=self.request.user)
        return reverse('pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class PatternDelete(DeleteView):
    model = Pattern
    template_name = 'pattern/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('patterns')


@login_required
def pattern_details(request, pk, tab_id: int):
    pattern = get_object_or_404(Pattern, id=pk)
    p_categories = PatternCategory.objects.filter(pattern=pattern).order_by('id')
    return render(request, 'pattern/pattern_details.html', {'pattern': pattern, 'p_categories': p_categories,
                                                            'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class PatternCategoryCreate(CreateView):
    model = PatternCategory
    form_class = PatternCategoryForm
    template_name = 'pattern/create.html'

    def get_initial(self):
        return {'pattern': self.kwargs.get('p_id'), 'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('pattern_details', kwargs={'pk': self.kwargs.get('p_id'), 'tab_id': 3})
        return context

    def get_success_url(self):
        self.object.update_timestamp(user=self.request.user)
        self.object.pattern.update_timestamp(user=self.request.user)
        return reverse('pattern_details', kwargs={'pk': self.object.pattern.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class PatternCategoryUpdate(UpdateView):
    model = PatternCategory
    form_class = PatternCategoryForm
    template_name = 'pattern/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('p_category_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        self.object.update_timestamp(user=self.request.user)
        self.object.pattern.update_timestamp(user=self.request.user)
        return reverse('pattern_details', kwargs={'pk': self.object.pattern.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class PatternCategoryDelete(DeleteView):
    model = PatternCategory
    template_name = 'pattern/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('p_category_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        self.object.pattern.update_timestamp(user=self.request.user)
        return reverse('pattern_details', kwargs={'pk': self.object.pattern.id, 'tab_id': 3})


@login_required
def p_category_details(request, pk, tab_id: int):
    p_category = get_object_or_404(PatternCategory, id=pk)
    return render(request, 'pattern/p_category_details.html', {'p_category': p_category, 'tab_id': tab_id})
