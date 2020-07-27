from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import FeatureList, FeatureListCategory, FeatureListItem, DeviceType
from .forms import FeatureListForm, FeatureListCategoryForm, FeatureListItemForm
from docx_builder.forms import DocxFeatureListForm
from redmine.forms import RedmineFeatureListForm
from django.urls import reverse
from datetime import datetime
from django.http import HttpResponseRedirect
from qa import settings
from django.utils.translation import gettext_lazy as _


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
        return {'device_type': self.kwargs.get('dt_id'), 'created_by': self.request.user,
                'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_type_details', kwargs={'pk': self.kwargs.get('dt_id'), 'tab_id': 3})
        return context

    def get_success_url(self):
        return reverse('device_type_details', kwargs={'pk': self.kwargs.get('dt_id'), 'tab_id': 3})


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
        return reverse('device_type_details', kwargs={'pk': self.object.device_type.id, 'tab_id': 3})


@login_required
def fl_details(request, pk, tab_id: int):
    feature_list = get_object_or_404(FeatureList, id=pk)
    categories = FeatureListCategory.objects.filter(feature_list=feature_list).order_by('id')
    docx_form = DocxFeatureListForm()
    redmine_form = RedmineFeatureListForm(initial={'project': feature_list.device_type.redmine_project,
                                                   'wiki': feature_list.redmine_wiki})
    redmine_url = settings.REDMINE_URL
    return render(request, 'feature/details.html', {'fl': feature_list, 'categories': categories,
                                                    'docx_form': docx_form,
                                                    'redmine_form': redmine_form,
                                                    'redmine_url': redmine_url,
                                                    'tab_id': tab_id})


@login_required
def fl_clone(request, pk):
    if request.method == 'POST':
        form = FeatureListForm(request.POST)
        if form.is_valid():
            new_fl = FeatureList(name=request.POST['name'],
                                 version=request.POST['version'],
                                 device_type=get_object_or_404(DeviceType, id=request.POST['device_type']),
                                 created_by=request.user,
                                 created_at=datetime.now(),
                                 updated_by=request.user,
                                 updated_at=datetime.now(),
                                 redmine_wiki=request.POST['redmine_wiki'])
            new_fl.save()
            src_fl = get_object_or_404(FeatureList, id=request.POST['src_fl'])
            src_categories = FeatureListCategory.objects.filter(feature_list=src_fl).order_by('id')
            for src_category in src_categories:
                new_category = FeatureListCategory(name=src_category.name, feature_list=new_fl)
                new_category.save()
                src_items = FeatureListItem.objects.filter(category=src_category).order_by('id')
                for src_item in src_items:
                    new_item = FeatureListItem(category=new_category, name=src_item.name, optional=src_item.optional)
                    new_item.save()
            return HttpResponseRedirect(reverse('fls'))
    else:
        feature_list = get_object_or_404(FeatureList, id=pk)
        form = FeatureListForm(initial={'name': feature_list.name, 'version': feature_list.version,
                                        'device_type': feature_list.device_type.id, 'created_by': request.user,
                                        'created_at': datetime.now(), 'updated_by': request.user,
                                        'updated_at': datetime.now(), 'redmine_wiki': feature_list.redmine_wiki})
        return render(request, 'feature/clone.html', {'form': form, 'fl_id': feature_list.id})


@login_required
def clear_fli(request, fl_id):
    feature_list = get_object_or_404(FeatureList, id=fl_id)
    if request.method == 'POST':
        feature_list.clear(user=request.user)
        return HttpResponseRedirect(reverse('fl_details', kwargs={'pk': fl_id, 'tab_id': 2}))
    else:
        back_url = reverse('fl_details', kwargs={'pk': fl_id, 'tab_id': 2})
        message = _('Are you sure?')
        return render(request, 'feature/clear.html', {'feature_list': feature_list, 'back_url': back_url,
                                                      'message': message})


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
    template_name = 'feature/update.html'

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
