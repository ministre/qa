from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import FeatureList, FeatureListCategory, FeatureListItem
from .forms import FeatureListForm, FeatureListCategoryForm, FeatureListItemForm
from django.urls import reverse
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class FeatureListListView(ListView):
    context_object_name = 'fls'
    queryset = FeatureList.objects.all().order_by('id')
    template_name = 'feature/list.html'


@method_decorator(login_required, name='dispatch')
class FeatureListCreate(CreateView):
    model = FeatureList
    form_class = FeatureListForm
    template_name = 'feature/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fls')
        return context

    def get_success_url(self):
        return reverse('fls')


@method_decorator(login_required, name='dispatch')
class FeatureListUpdate(UpdateView):
    model = FeatureList
    form_class = FeatureListForm
    template_name = 'feature/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fl_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        self.object.update_timestamp(user=self.request.user)
        return reverse('fl_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class FeatureListDelete(DeleteView):
    model = FeatureList
    template_name = 'feature/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fl_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('fls')


@login_required
def fl_details(request, pk, tab_id: int):
    feature_list = get_object_or_404(FeatureList, id=pk)
    categories = FeatureListCategory.objects.filter(feature_list=feature_list).order_by('id')
    return render(request, 'feature/details.html', {'fl': feature_list, 'categories': categories, 'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class FeatureListCategoryCreate(CreateView):
    model = FeatureListCategory
    form_class = FeatureListCategoryForm
    template_name = 'feature/create.html'

    def get_initial(self):
        return {'feature_list': self.kwargs.get('fl_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fl_details', kwargs={'pk': self.kwargs.get('fl_id'), 'tab_id': 2})
        return context

    def get_success_url(self):
        self.object.feature_list.update_timestamp(user=self.request.user)
        return reverse('fl_details', kwargs={'pk': self.object.feature_list.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class FeatureListCategoryUpdate(UpdateView):
    model = FeatureListCategory
    form_class = FeatureListCategoryForm
    template_name = 'feature/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fl_details', kwargs={'pk': self.object.feature_list.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        self.object.feature_list.update_timestamp(user=self.request.user)
        return reverse('fl_details', kwargs={'pk': self.object.feature_list.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class FeatureListCategoryDelete(DeleteView):
    model = FeatureListCategory
    template_name = 'feature/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fl_details', kwargs={'pk': self.object.feature_list.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        self.object.feature_list.update_timestamp(user=self.request.user)
        return reverse('fl_details', kwargs={'pk': self.object.feature_list.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class FeatureListItemCreate(CreateView):
    model = FeatureListItem
    form_class = FeatureListItemForm
    template_name = 'feature/create.html'

    def get_initial(self):
        return {'category': self.kwargs.get('category_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(FeatureListCategory, id=self.kwargs.get('category_id'))
        context['back_url'] = reverse('fl_details', kwargs={'pk': category.feature_list.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        self.object.category.feature_list.update_timestamp(user=self.request.user)
        return reverse('fl_details', kwargs={'pk': self.object.category.feature_list.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class FeatureListItemUpdate(UpdateView):
    model = FeatureListItem
    form_class = FeatureListItemForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fl_details', kwargs={'pk': self.object.category.feature_list.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        self.object.category.feature_list.update_timestamp(user=self.request.user)
        return reverse('fl_details', kwargs={'pk': self.object.category.feature_list.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class FeatureListItemDelete(DeleteView):
    model = FeatureListItem
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('fl_details', kwargs={'pk': self.object.category.feature_list.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        feature_list = self.object.category.feature_list
        feature_list.update_timestamp(user=self.request.user)
        return reverse('fl_details', kwargs={'pk': feature_list.id, 'tab_id': 2})
