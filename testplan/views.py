from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from testplan.models import TestplanChecklist, Testplan, TestplanCategory, TestplanChapter, Test
from .forms import TestplanForm, TestplanCategoryForm, TestplanChapterForm, TestForm
from django.shortcuts import get_object_or_404
import textile
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class TestplanListView(ListView):
    context_object_name = 'testplans'
    queryset = Testplan.objects.all()
    template_name = 'testplan/testplans.html'


@method_decorator(login_required, name='dispatch')
class TestplanCreate(CreateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('testplans')


@method_decorator(login_required, name='dispatch')
class TestplanDelete(DeleteView):
    model = Testplan
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse('testplans')


@method_decorator(login_required, name='dispatch')
class TestplanUpdate(UpdateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('pk')
        return context

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('pk'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('pk')})


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
    amount_of_tests = count_of_tests(pk)
    return render(request, 'testplan/testplan_details.html', {'testplan': testplan, 'categories': categories,
                                                              'chapters': chapters, 'amount_of_tests': amount_of_tests})


@method_decorator(login_required, name='dispatch')
class CategoryCreate(CreateView):
    model = TestplanCategory
    form_class = TestplanCategoryForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('testplan')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class CategoryDelete(DeleteView):
    model = TestplanCategory
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class CategoryUpdate(UpdateView):
    model = TestplanCategory
    form_class = TestplanCategoryForm
    template_name = 'testplan/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestCreate(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'category': self.kwargs.get('pk')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestDelete(DeleteView):
    model = Test
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestUpdate(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'testplan/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@login_required
def test_details(request, testplan, pk):
    test = get_object_or_404(Test, id=pk)
    testplan = get_object_or_404(Test, id=testplan)
    category = test.category
    test_procedure = textile.textile(test.procedure)
    test_expected = textile.textile(test.expected)
    return render(request, 'testplan/test_details.html', {'testplan': testplan, 'category': category,
                                                          'test': test, 'test_procedure': test_procedure,
                                                          'test_expected': test_expected})


# Return amount of tests in testplan
def count_of_tests(testplan_id):
    count = 0
    categories = TestplanCategory.objects.filter(testplan=Testplan.objects.get(id=testplan_id))
    for category in categories:
        tests = Test.objects.filter(category=TestplanCategory.objects.get(id=category.id))
        for test in tests:
            count += 1
    return count


# Update testplan fields 'updated_by' and 'updated_at'
def testplan_update_timestamp(testplan_id, user):
    testplan = Testplan.objects.get(id=testplan_id)
    testplan.updated_by = user
    testplan.updated_at = datetime.now()
    testplan.save()
    return True


@method_decorator(login_required, name='dispatch')
class ChapterCreate(CreateView):
    model = TestplanChapter
    form_class = TestplanChapterForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('testplan')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class ChapterDelete(DeleteView):
    model = TestplanChapter
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class ChapterUpdate(UpdateView):
    model = TestplanChapter
    form_class = TestplanChapterForm
    template_name = 'testplan/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class TestplanChecklistListView(ListView):
    context_object_name = 'testplan_checklists'
    queryset = TestplanChecklist.objects.all()
    template_name = 'testplan/checklists.html'
