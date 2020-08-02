from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Pattern, PatternCategory
from .forms import PatternForm, PatternCategoryForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.http import HttpResponseRedirect
from django.db.models import Max, Min


class Item(object):
    @staticmethod
    def update_timestamp(foo, user):
        foo.updated_by = user
        foo.updated_at = datetime.now()
        foo.save()

    @staticmethod
    def set_priority(foo, priority: int):
        foo.priority = priority
        foo.save()


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
        Item.update_timestamp(foo=self.object, user=self.request.user)
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
    p_categories = PatternCategory.objects.filter(pattern=pattern).order_by('priority')
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
        Item.set_priority(foo=self.object, priority=self.object.id)
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.pattern, user=self.request.user)
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
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.pattern, user=self.request.user)
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
        Item.update_timestamp(foo=self.object.pattern, user=self.request.user)
        return reverse('pattern_details', kwargs={'pk': self.object.pattern.id, 'tab_id': 3})


@login_required
def p_category_details(request, pk, tab_id: int):
    p_category = get_object_or_404(PatternCategory, id=pk)
    return render(request, 'pattern/p_category_details.html', {'p_category': p_category, 'tab_id': tab_id})


@login_required
def p_category_up(request, pk):
    p_category = get_object_or_404(PatternCategory, id=pk)
    pre_categories = PatternCategory.objects.filter(pattern=p_category.pattern,
                                                    priority__lt=p_category.priority).aggregate(Max('priority'))
    pre_p_category = get_object_or_404(PatternCategory, pattern=p_category.pattern,
                                       priority=pre_categories['priority__max'])
    Item.set_priority(foo=pre_p_category, priority=p_category.priority)
    Item.set_priority(foo=p_category, priority=pre_categories['priority__max'])
    return HttpResponseRedirect(reverse('pattern_details', kwargs={'pk': p_category.pattern.id, 'tab_id': 3}))


@login_required
def p_category_down(request, pk):
    p_category = get_object_or_404(PatternCategory, id=pk)
    next_categories = PatternCategory.objects.filter(pattern=p_category.pattern,
                                                     priority__gt=p_category.priority).aggregate(Min('priority'))
    next_p_category = get_object_or_404(PatternCategory, pattern=p_category.pattern,
                                        priority=next_categories['priority__min'])
    Item.set_priority(foo=next_p_category, priority=p_category.priority)
    Item.set_priority(foo=p_category, priority=next_categories['priority__min'])
    return HttpResponseRedirect(reverse('pattern_details', kwargs={'pk': p_category.pattern.id, 'tab_id': 3}))
