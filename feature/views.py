from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import FeatureList, FeatureListCategory, FeatureListItem
from .forms import FeatureListForm, FeatureListCategoryForm
from django.urls import reverse
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class FeatureListCreate(CreateView):
    model = FeatureList
    form_class = FeatureListForm
    template_name = 'feature_list/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('feature_lists')


@method_decorator(login_required, name='dispatch')
class FeatureListListView(ListView):
    context_object_name = 'feature_lists'
    queryset = FeatureList.objects.all().order_by('id')
    template_name = 'feature_list/list.html'


@method_decorator(login_required, name='dispatch')
class FeatureListUpdate(UpdateView):
    model = FeatureList
    form_class = FeatureListForm
    template_name = 'feature_list/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        return reverse('feature_lists')


@method_decorator(login_required, name='dispatch')
class FeatureListDelete(DeleteView):
    model = FeatureList
    template_name = 'feature_list/delete.html'

    def get_success_url(self):
        return reverse('feature_lists')


@login_required
def feature_list_details(request, pk):
    feature_list = get_object_or_404(FeatureList, id=pk)
    categories = get_feature_list_items(pk)
    return render(request, 'feature_list/details.html', {'feature_list': feature_list,
                                                         'categories': categories})


@method_decorator(login_required, name='dispatch')
class FeatureListCategoryCreate(CreateView):
    model = FeatureListCategory
    form_class = FeatureListCategoryForm
    template_name = 'feature_list_category/create.html'

    def get_initial(self):
        return {'feature_list': self.kwargs.get('feature_list_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature_list_id'] = self.kwargs.get('feature_list_id')
        return context

    def get_success_url(self):
        feature_list_update_timestamp(self.kwargs.get('feature_list_id'), self.request.user)
        return reverse('feature_list_details', kwargs={'pk': self.kwargs.get('feature_list_id')})


@method_decorator(login_required, name='dispatch')
class FeatureListCategoryDelete(DeleteView):
    model = FeatureListCategory
    template_name = 'feature_list_category/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature_list_id'] = self.kwargs.get('feature_list_id')
        return context

    def get_success_url(self):
        feature_list_update_timestamp(self.kwargs.get('feature_list_id'), self.request.user)
        return reverse('feature_list_details', kwargs={'pk': self.kwargs.get('feature_list_id')})


@method_decorator(login_required, name='dispatch')
class FeatureListCategoryUpdate(UpdateView):
    model = FeatureListCategory
    form_class = FeatureListCategoryForm
    template_name = 'feature_list_category/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature_list_id'] = self.kwargs.get('feature_list_id')
        return context

    def get_success_url(self):
        feature_list_update_timestamp(self.kwargs.get('feature_list_id'), self.request.user)
        return reverse('feature_list_details', kwargs={'pk': self.kwargs.get('feature_list_id')})


def feature_list_update_timestamp(feature_list_id, user):
    feature_list = FeatureList.objects.get(id=feature_list_id)
    feature_list.updated_by = user
    feature_list.updated_at = datetime.now()
    feature_list.save()
    return True


def get_feature_list_items(feature_list_id):
    feature_list = get_object_or_404(FeatureList, id=feature_list_id)
    feature_list_categories = FeatureListCategory.objects.filter(feature_list=feature_list).order_by('id')
    feature_list_items = []
    for feature_list_category in feature_list_categories:
        items = FeatureListItem.objects.filter(feature_list_category=feature_list_category).order_by('id')
        feature_list_items.append({'id': feature_list_category.id, 'name': feature_list_category.name, 'items': items})
    return feature_list_items
