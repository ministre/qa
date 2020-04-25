from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Testplan, Category, Chapter, Test, TestConfig, TestImage, TestFile, TestWorksheet, \
    TestWorksheetItem, TestLink, TestComment, Pattern
from .forms import TestplanForm, CategoryForm, ChapterForm, TestForm, TestConfigForm, TestImageForm, TestFileForm,\
    TestWorksheetForm, WorksheetItemForm, TestLinkForm, TestCommentForm, PatternForm
from django.http import HttpResponseRedirect
import textile
from datetime import datetime
from redmine.models import RedmineProject


@login_required
def testplan_list(request, tab_id):
    testplans = Testplan.objects.all().order_by("id")
    patterns = Pattern.objects.all().order_by("id")
    return render(request, 'testplan/list.html', {'testplans': testplans, 'patterns': patterns,
                                                  'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class TestplanCreate(CreateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestplanDelete(DeleteView):
    model = Testplan
    template_name = 'testplan/delete.html'

    def get_success_url(self):
        return reverse('testplans', kwargs={'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TestplanUpdate(UpdateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.object.id)
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 1})


def get_testlist(testplan: Testplan):
    categories = Category.objects.filter(testplan=testplan).order_by('id')
    testlist = []
    for category in categories:
        tests = Test.objects.filter(category=category).order_by('id')
        testlist.append({'id': category.id, 'name': category.name, 'tests': tests})
    return testlist


def get_full_worksheets(test_id):
    test = get_object_or_404(Test, id=test_id)
    worksheets = TestWorksheet.objects.filter(test=test).order_by('id')
    full_worksheets = []
    for worksheet in worksheets:
        items = TestWorksheetItem.objects.filter(worksheet=worksheet).order_by('id')
        full_worksheets.append({'id': worksheet.id, 'name': worksheet.name, 'items': items})
    return full_worksheets


@login_required
def testplan_details(request, pk, tab_id):
    testplan = get_object_or_404(Testplan, id=pk)
    chapters = Chapter.objects.filter(testplan=testplan).order_by('id')
    categories = get_testlist(testplan)
    amount_of_tests = tests_count(testplan)
    r = RedmineProject(testplan.redmine_project)
    return render(request, 'testplan/details.html', {'tab_id': tab_id, 'testplan': testplan, 'categories': categories,
                                                     'chapters': chapters, 'amount_of_tests': amount_of_tests,
                                                     'redmine_wiki': r.get_wiki_url('wiki')})


@login_required
def pattern_details(request, pk, tab_id):
    pattern = get_object_or_404(Pattern, id=pk)
    r = RedmineProject(pattern.redmine_project)
    return render(request, 'pattern/details.html', {'tab_id': tab_id, 'pattern': pattern,
                                                    'redmine_wiki': r.get_wiki_url('wiki')})


@method_decorator(login_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('testplan_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestCreate(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'test/create.html'

    def get_initial(self):
        return {'category': self.kwargs.get('category_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TestDelete(DeleteView):
    model = Test
    template_name = 'test/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestUpdate(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'test/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': self.object.id, 'tab_id': 1})


@login_required
def test_details(request, testplan_id, pk, tab_id):
    test = get_object_or_404(Test, id=pk)
    testplan = get_object_or_404(Testplan, id=testplan_id)
    test_procedure = textile.textile(test.procedure)
    test_expected = textile.textile(test.expected)
    configs = TestConfig.objects.filter(test=test).order_by('id')
    images = TestImage.objects.filter(test=test).order_by('id')
    files = TestFile.objects.filter(test=test).order_by('id')
    worksheets = get_full_worksheets(pk)
    links = TestLink.objects.filter(test=test).order_by('id')
    comments = TestComment.objects.filter(test=test).order_by('id')
    for comment in comments:
        comment.text = textile.textile(comment.text)
    r = RedmineProject(testplan.redmine_project)
    return render(request, 'test/details.html', {'tab_id': tab_id, 'testplan': testplan, 'test': test,
                                                 'test_procedure': test_procedure, 'test_expected': test_expected,
                                                 'configs': configs, 'images': images, 'files': files,
                                                 'worksheets': worksheets, 'links': links, 'comments': comments,
                                                 'redmine_wiki': r.get_wiki_url(test.redmine_wiki)})


@login_required
def chapter_details(request, testplan_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    testplan = get_object_or_404(Testplan, id=testplan_id)
    chapter_text = textile.textile(chapter.text)
    return render(request, 'chapter/details.html', {'chapter': chapter, 'testplan': testplan,
                                                    'chapter_text': chapter_text})


def tests_count(testplan: Testplan):
    count = 0
    for category in Category.objects.filter(testplan=testplan):
        tests = Test.objects.filter(category=category)
        count += tests.count()
    return count


@method_decorator(login_required, name='dispatch')
class ChapterCreate(CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'chapter/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('testplan_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ChapterDelete(DeleteView):
    model = Chapter
    template_name = 'chapter/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ChapterUpdate(UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'chapter/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        return context

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 2})


@login_required
def clear_tests(request, testplan_id):
    testplan = get_object_or_404(Testplan, id=testplan_id)
    if request.method == 'POST':
        Category.objects.filter(testplan=testplan).delete()
        testplan.update_timestamp(user=request.user)
        return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': testplan_id, 'tab_id': 3}))
    else:
        return render(request, 'test/clear.html', {'testplan': testplan})


@login_required
def clear_chapters(request, testplan_id):
    testplan = get_object_or_404(Testplan, id=testplan_id)
    if request.method == 'POST':
        Chapter.objects.filter(testplan=testplan).delete()
        testplan.update_timestamp(user=request.user)
        return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': testplan_id, 'tab_id': 2}))
    else:
        return render(request, 'chapter/clear.html', {'testplan': testplan})


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
        context['tab_id'] = 5
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class TestConfigDelete(DeleteView):
    model = TestConfig
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 5
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 5})


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
        context['tab_id'] = 5
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 5})


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
        context['tab_id'] = 6
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestImageDelete(DeleteView):
    model = TestImage
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 6
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 6})


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
        context['tab_id'] = 6
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 6})


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
        context['tab_id'] = 7
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class TestFileDelete(DeleteView):
    model = TestFile
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 7
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 7})


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
        context['tab_id'] = 7
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class TestWorksheetCreate(CreateView):
    model = TestWorksheet
    form_class = TestWorksheetForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 8
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestWorksheetDelete(DeleteView):
    model = TestWorksheet
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 8
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestWorksheetUpdate(UpdateView):
    model = TestWorksheet
    form_class = TestWorksheetForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 8
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class WorksheetItemCreate(CreateView):
    model = TestWorksheetItem
    form_class = WorksheetItemForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'worksheet': self.kwargs.get('worksheet_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['worksheet_id'] = self.kwargs.get('worksheet_id')
        context['tab_id'] = 8
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class WorksheetItemDelete(DeleteView):
    model = TestWorksheetItem
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 8
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class WorksheetItemUpdate(UpdateView):
    model = TestWorksheetItem
    form_class = WorksheetItemForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 8
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 8})


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
        context['tab_id'] = 9
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 9})


@method_decorator(login_required, name='dispatch')
class TestLinkDelete(DeleteView):
    model = TestLink
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 9
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 9})


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
        context['tab_id'] = 9
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 9})


@method_decorator(login_required, name='dispatch')
class TestCommentCreate(CreateView):
    model = TestComment
    form_class = TestCommentForm
    template_name = 'test_component/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 10
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 10})


@method_decorator(login_required, name='dispatch')
class TestCommentDelete(DeleteView):
    model = TestComment
    template_name = 'test_component/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 10
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 10})


@method_decorator(login_required, name='dispatch')
class TestCommentUpdate(UpdateView):
    model = TestComment
    form_class = TestCommentForm
    template_name = 'test_component/update.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testplan_id'] = self.kwargs.get('testplan_id')
        context['test_id'] = self.kwargs.get('test_id')
        context['tab_id'] = 10
        return context

    def get_success_url(self):
        test = get_object_or_404(Test, id=self.kwargs.get('test_id'))
        test.update_timestamp(user=self.request.user)
        testplan = get_object_or_404(Testplan, id=self.kwargs.get('testplan_id'))
        testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'testplan_id': testplan.id, 'pk': test.id, 'tab_id': 10})


@method_decorator(login_required, name='dispatch')
class PatternCreate(CreateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'pattern/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class PatternDelete(DeleteView):
    model = Pattern
    template_name = 'pattern/delete.html'

    def get_success_url(self):
        return reverse('testplans', kwargs={'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class PatternUpdate(UpdateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'pattern/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        pattern = get_object_or_404(Pattern, id=self.object.id)
        pattern.update_timestamp(user=self.request.user)
        return reverse('pattern_details', kwargs={'pk': pattern.id, 'tab_id': 1})
