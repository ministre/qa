from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from testplan.models import Checklist, Testplan, Category, Chapter, Test
from .forms import TestplanForm, CategoryForm, ChapterForm, TestForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
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
    categories = Category.objects.filter(testplan=testplan).order_by('id')
    testlist = []
    for category in categories:
        tests = Test.objects.filter(category=category).order_by('id')
        testlist.append({'id': category.id, 'name': category.name, 'tests': tests})
    return testlist


@login_required
def testplan_details(request, pk):
    testplan = get_object_or_404(Testplan, id=pk)
    chapters = Chapter.objects.filter(testplan=testplan).order_by('id')
    categories = get_testlist(pk)
    amount_of_tests = count_of_tests(pk)
    return render(request, 'testplan/testplan_details.html', {'testplan': testplan, 'categories': categories,
                                                              'chapters': chapters, 'amount_of_tests': amount_of_tests})


@method_decorator(login_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
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
    model = Category
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
    model = Category
    form_class = CategoryForm
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
    testplan = get_object_or_404(Testplan, id=testplan)
    test_procedure = textile.textile(test.procedure)
    test_expected = textile.textile(test.expected)
    return render(request, 'testplan/test_details.html', {'testplan': testplan, 'test': test,
                                                          'test_procedure': test_procedure,
                                                          'test_expected': test_expected})


@login_required
def chapter_details(request, testplan, pk):
    chapter = get_object_or_404(Chapter, id=pk)
    testplan = get_object_or_404(Testplan, id=testplan)
    chapter_text = textile.textile(chapter.text)
    return render(request, 'testplan/chapter_details.html', {'chapter': chapter, 'testplan': testplan,
                                                             'chapter_text': chapter_text})


# Return amount of tests in testplan
def count_of_tests(testplan_id):
    count = 0
    categories = Category.objects.filter(testplan=Testplan.objects.get(id=testplan_id))
    for category in categories:
        tests = Test.objects.filter(category=Category.objects.get(id=category.id))
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
    model = Chapter
    form_class = ChapterForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('testplan'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@method_decorator(login_required, name='dispatch')
class ChapterDelete(DeleteView):
    model = Chapter
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
    model = Chapter
    form_class = ChapterForm
    template_name = 'testplan/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan')
        return context

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan'), self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan')})


@login_required
def clear_tests(request, testplan):
    if request.method == 'POST':
        Category.objects.filter(testplan=Testplan.objects.get(id=testplan)).delete()
        testplan_update_timestamp(testplan, request.user)
        return HttpResponseRedirect('/testplan/' + str(testplan) + '/')
    else:
        message = 'Delete all tests in testplan #' + str(testplan) + '?'
        return render(request, 'testplan/clear.html', {'message': message, 'testplan_id': testplan})


@login_required
def clear_chapters(request, testplan):
    if request.method == 'POST':
        Chapter.objects.filter(testplan=Testplan.objects.get(id=testplan)).delete()
        testplan_update_timestamp(testplan, request.user)
        return HttpResponseRedirect('/testplan/' + str(testplan) + '/')
    else:
        message = 'Delete all chapters in testplan #' + str(testplan) + '?'
        return render(request, 'testplan/clear.html', {'message': message, 'testplan_id': testplan})


@method_decorator(login_required, name='dispatch')
class ChecklistListView(ListView):
    context_object_name = 'checklists'
    queryset = Checklist.objects.all()
    template_name = 'testplan/checklists.html'
