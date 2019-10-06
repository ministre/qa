from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from testplan.models import TestplanPattern, TestplanPatternCategory, TestplanChecklist, Testplan, TestplanCategory, \
    TestplanChapter, Test
from .forms import TestplanPatternForm, TestplanPatternCategoryForm, TestplanForm, TestplanCategoryForm, \
    TestplanChapterForm, TestForm
from django.shortcuts import get_object_or_404
from django.db.models import Max
from django.http import HttpResponseRedirect


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


@login_required
def testplan_pattern_details(request, pk):
    pattern = get_object_or_404(TestplanPattern, id=pk)
    categories = TestplanPatternCategory.objects.filter(pattern=pattern)
    return render(request, 'testplan/testplan_pattern_details.html', {'pk': pk, 'categories': categories,
                                                                      'pattern': pattern})


@login_required
def testplan_pattern_category_create(request, pk):
    if request.method == "POST":
        form = TestplanPatternCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/testplan/pattern/' + str(pk) + '/')
    else:
        pattern = TestplanPattern.objects.get(pk=pk)
        categories = TestplanPatternCategory.objects.filter(pattern=pattern)
        if categories:
            queue = categories.aggregate(Max('queue')).get('queue__max')+1
        else:
            queue = 0
        form = TestplanPatternCategoryForm(initial={'pattern': pattern.id, 'queue': queue})
        return render(request, 'testplan/testplan_pattern_category_create.html', {'form': form, 'pk': pk})


@method_decorator(login_required, name='dispatch')
class TestplanPatternCategoryUpdate(UpdateView):
    model = TestplanPatternCategory
    form_class = TestplanPatternCategoryForm
    template_name = 'testplan/testplan_pattern_category_update.html'

    def get_success_url(self):
        return reverse('testplan_pattern_list')


@method_decorator(login_required, name='dispatch')
class TestplanChecklistListView(ListView):
    context_object_name = 'testplan_checklists'
    queryset = TestplanChecklist.objects.all()
    template_name = 'testplan/testplan_checklist_list.html'


@method_decorator(login_required, name='dispatch')
class TestplanListView(ListView):
    context_object_name = 'testplans'
    queryset = Testplan.objects.all()
    template_name = 'testplan/testplan_list.html'


@method_decorator(login_required, name='dispatch')
class TestplanCreate(CreateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'created_by': self.request.user}

    def get_success_url(self):
        return reverse('testplan_list')


def get_testlist(testplan_id):
    testplan = get_object_or_404(Testplan, id=testplan_id)
    categories = TestplanCategory.objects.filter(testplan=testplan).order_by('id')
    testlist = []
    for category in categories:
        tests = Test.objects.filter(category=category).order_by('id')
        testlist.append({'id': category.id, 'name': category.name, 'tests': tests})
    return testlist


@login_required
def testplan_details(request, pk):
    testplan = get_object_or_404(Testplan, id=pk)
    chapters = TestplanChapter.objects.filter(testplan=testplan).order_by('id')
    categories = get_testlist(pk)

    return render(request, 'testplan/testplan_details.html', {'testplan': testplan, 'categories': categories,
                                                              'chapters': chapters})


@method_decorator(login_required, name='dispatch')
class TestplanUpdate(UpdateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/update.html'

    def get_success_url(self):
        return reverse('testplan_list')


@method_decorator(login_required, name='dispatch')
class TestplanDelete(DeleteView):
    model = Testplan
    template_name = 'testplan/delete.html'

    def get_success_url(self):
        return reverse('testplan_list')


@method_decorator(login_required, name='dispatch')
class TestplanCategoryCreate(CreateView):
    model = TestplanCategory
    form_class = TestplanCategoryForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('pk')}

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('pk')})


@method_decorator(login_required, name='dispatch')
class TestplanCategoryUpdate(UpdateView):
    model = TestplanCategory
    form_class = TestplanCategoryForm
    template_name = 'testplan/update.html'

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestplanCategoryDelete(DeleteView):
    model = TestplanCategory
    template_name = 'testplan/delete.html'

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestplanChapterCreate(CreateView):
    model = TestplanChapter
    form_class = TestplanChapterForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('pk')}

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('pk')})


@method_decorator(login_required, name='dispatch')
class TestplanChapterUpdate(UpdateView):
    model = TestplanChapter
    form_class = TestplanChapterForm
    template_name = 'testplan/update.html'

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestplanChapterDelete(DeleteView):
    model = TestplanChapter
    template_name = 'testplan/delete.html'

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestCreate(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'category': self.kwargs.get('pk')}

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan_id')})
