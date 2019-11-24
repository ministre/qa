from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from testplan.models import Testplan, Category, Chapter, Test, TestConfig, TestImage, TestFile, TestChecklist, \
    ChecklistItem, TestLink, Pattern
from .forms import TestplanForm, CategoryForm, ChapterForm, TestForm, TestConfigForm, TestImageForm, TestFileForm, \
    TestChecklistForm, ChecklistItemForm, TestLinkForm, PatternForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import textile
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class TestplanListView(ListView):
    context_object_name = 'testplans'
    queryset = Testplan.objects.all()
    template_name = 'testplan/list.html'


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
def testplan_details(request, testplan_id):
    testplan = get_object_or_404(Testplan, id=testplan_id)
    chapters = Chapter.objects.filter(testplan=testplan).order_by('id')
    categories = get_testlist(testplan_id)
    amount_of_tests = count_of_tests(testplan_id)
    return render(request, 'testplan/details.html', {'testplan': testplan, 'categories': categories,
                                                     'chapters': chapters, 'amount_of_tests': amount_of_tests})


@method_decorator(login_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'

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
    template_name = 'category/delete.html'

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
    template_name = 'category/update.html'

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
    template_name = 'test/create.html'

    def get_initial(self):
        return {'category': self.kwargs.get('pk'),
                'created_by': self.request.user, 'updated_by': self.request.user}

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
    template_name = 'test/delete.html'

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
    template_name = 'test/update.html'

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
def test_details(request, testplan_id, test_id):
    test = get_object_or_404(Test, id=test_id)
    testplan = get_object_or_404(Testplan, id=testplan_id)
    test_procedure = textile.textile(test.procedure)
    test_expected = textile.textile(test.expected)
    configs = TestConfig.objects.filter(test=test).order_by('id')
    images = TestImage.objects.filter(test=test).order_by('id')
    files = TestFile.objects.filter(test=test).order_by('id')
    checklists = TestChecklist.objects.filter(test=test).order_by('id')
    links = TestLink.objects.filter(test=test).order_by('id')
    return render(request, 'test/details.html', {'testplan': testplan, 'test': test, 'test_procedure': test_procedure,
                                                 'test_expected': test_expected, 'configs': configs, 'images': images,
                                                 'files': files, 'checklists': checklists, 'links': links})


@login_required
def chapter_details(request, testplan, pk):
    chapter = get_object_or_404(Chapter, id=pk)
    testplan = get_object_or_404(Testplan, id=testplan)
    chapter_text = textile.textile(chapter.text)
    return render(request, 'chapter/details.html', {'chapter': chapter, 'testplan': testplan,
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


# Update test fields 'updated_by' and 'updated_at'
def test_update_timestamp(test_id, user):
    test = Test.objects.get(id=test_id)
    test.updated_by = user
    test.updated_at = datetime.now()
    test.save()
    return True


@method_decorator(login_required, name='dispatch')
class ChapterCreate(CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'test/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('testplan_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('testplan_details', kwargs={'testplan_id': self.kwargs.get('testplan_id')})


@method_decorator(login_required, name='dispatch')
class ChapterDelete(DeleteView):
    model = Chapter
    template_name = 'test/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('testplan_details', kwargs={'testplan_id': self.kwargs.get('testplan_id')})


@method_decorator(login_required, name='dispatch')
class ChapterUpdate(UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'test/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('testplan_details', kwargs={'testplan_id': self.kwargs.get('testplan_id')})


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
def clear_chapters(request, testplan_id):
    if request.method == 'POST':
        Chapter.objects.filter(testplan=Testplan.objects.get(id=testplan_id)).delete()
        testplan_update_timestamp(testplan_id, request.user)
        return HttpResponseRedirect('/testplan/' + str(testplan_id) + '/')
    else:
        message = 'Delete all chapters in testplan #' + str(testplan_id) + '?'
        return render(request, 'testplan/clear.html', {'message': message, 'testplan_id': testplan_id})


@method_decorator(login_required, name='dispatch')
class TestConfigCreate(CreateView):
    model = TestConfig
    form_class = TestConfigForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestConfigDelete(DeleteView):
    model = TestConfig
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestConfigUpdate(UpdateView):
    model = TestConfig
    form_class = TestConfigForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestImageCreate(CreateView):
    model = TestImage
    form_class = TestImageForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestImageDelete(DeleteView):
    model = TestImage
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestImageUpdate(UpdateView):
    model = TestImage
    form_class = TestImageForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestFileCreate(CreateView):
    model = TestFile
    form_class = TestFileForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestFileDelete(DeleteView):
    model = TestFile
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestFileUpdate(UpdateView):
    model = TestFile
    form_class = TestFileForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestChecklistCreate(CreateView):
    model = TestChecklist
    form_class = TestChecklistForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestChecklistDelete(DeleteView):
    model = TestChecklist
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestChecklistUpdate(UpdateView):
    model = TestChecklist
    form_class = TestChecklistForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class ChecklistItemCreate(CreateView):
    model = ChecklistItem
    form_class = ChecklistItemForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'checklist': self.kwargs.get('checklist_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['checklist_id'] = self.kwargs.get('checklist_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestLinkCreate(CreateView):
    model = TestLink
    form_class = TestLinkForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestLinkDelete(DeleteView):
    model = TestLink
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


@method_decorator(login_required, name='dispatch')
class TestLinkUpdate(UpdateView):
    model = TestLink
    form_class = TestLinkForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        return context

    def get_success_url(self):
        test_update_timestamp(self.kwargs.get('test_id'), self.request.user)
        testplan_update_timestamp(self.kwargs.get('testplan_id'), self.request.user)
        return reverse('test_details', kwargs={'testplan_id': self.kwargs.get('testplan_id'),
                                               'test_id': self.kwargs.get('test_id')})


# patterns

@method_decorator(login_required, name='dispatch')
class PatternListView(ListView):
    context_object_name = 'patterns'
    queryset = Pattern.objects.all().order_by('id')
    template_name = 'pattern/list.html'


@method_decorator(login_required, name='dispatch')
class PatternCreate(CreateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('patterns')
