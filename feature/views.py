from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import FeatureList
from .forms import FeatureListForm
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
#    chapters = Chapter.objects.filter(testplan=testplan).order_by('id')
#    categories = get_testlist(testplan_id)
    return render(request, 'feature_list/details.html', {'feature_list': feature_list})
