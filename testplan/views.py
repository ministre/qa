from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Testplan, Category, Chapter, Test, TestConfig, TestImage, TestFile, TestChecklist, \
    TestChecklistItem, TestIntegerValue, TestLink, TestComment, Pattern, DeviceType
from .forms import TestplanForm, CategoryForm, ChapterForm, TestForm, TestConfigForm, TestImageForm, TestFileForm,\
    TestChecklistForm, TestChecklistItemForm, TestIntegerValueForm, TestLinkForm, TestCommentForm, \
    PatternForm
from docx_builder.forms import DocxTestplanForm
from redmine.forms import RedmineChapterForm, RedmineTestForm, RedmineExportTestplanForm, RedmineImportTestplanForm
from django.http import HttpResponseRedirect
import textile
from datetime import datetime
from redmine.models import RedmineProject
from qa import settings
from django.utils.translation import gettext_lazy as _


@login_required
def testplan_list(request, tab_id):
    testplans = Testplan.objects.all().order_by('id')
    patterns = Pattern.objects.all().order_by('id')
    return render(request, 'testplan/list.html', {'testplans': testplans, 'patterns': patterns, 'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class TestplanCreate(CreateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplans', kwargs={'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestplanDelete(DeleteView):
    model = Testplan
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('testplans', kwargs={'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TestplanUpdate(UpdateView):
    model = Testplan
    form_class = TestplanForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        self.object.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@login_required
def testplan_details(request, pk, tab_id):
    testplan = get_object_or_404(Testplan, id=pk)
    chapters = Chapter.objects.filter(testplan=testplan).order_by('id')
    categories = Category.objects.filter(testplan=testplan).order_by('id')
    protocols_count = testplan.protocols_count()
    redmine_export_form = RedmineExportTestplanForm(initial={'parent': testplan.redmine_parent,
                                                             'project': testplan.redmine_project,
                                                             'chapters': True,
                                                             'tests': True})
    redmine_import_form = RedmineImportTestplanForm(initial={'parent': testplan.redmine_parent,
                                                             'project': testplan.redmine_project,
                                                             'chapters': True,
                                                             'tests': True})
    redmine_url = settings.REDMINE_URL
    docx_form = DocxTestplanForm(initial={'page_header': True, 'convert_textile': True, 'chapters': True,
                                          'purpose': True, 'procedure': True, 'expected': True, 'configs': True,
                                          'images': True, 'checklists': True, 'links': True, 'comments': False})
    return render(request, 'testplan/testplan_details.html', {'tab_id': tab_id, 'testplan': testplan,
                                                              'categories': categories,
                                                              'chapters': chapters,
                                                              'tests_count': testplan.tests_count(),
                                                              'protocols_count': protocols_count,
                                                              'docx_form': docx_form,
                                                              'redmine_export_form': redmine_export_form,
                                                              'redmine_import_form': redmine_import_form,
                                                              'redmine_url': redmine_url})


@login_required
def testplan_clone(request, pk):
    if request.method == 'POST':
        form = TestplanForm(request.POST)
        if form.is_valid():
            new_testplan = Testplan(name=request.POST['name'],
                                    version=request.POST['version'],
                                    device_type=get_object_or_404(DeviceType, id=request.POST['device_type']),
                                    created_by=request.user,
                                    created_at=datetime.now(),
                                    updated_by=request.user,
                                    updated_at=datetime.now(),
                                    redmine_parent=request.POST['redmine_parent'],
                                    redmine_project=request.POST['redmine_project']
                                    )
            new_testplan.save()

            src_testplan = get_object_or_404(Testplan, id=request.POST['src_testplan'])
            src_categories = Category.objects.filter(testplan=src_testplan).order_by('id')
            for src_category in src_categories:
                new_category = Category(name=src_category.name, testplan=new_testplan)
                new_category.save()

                src_tests = Test.objects.filter(category=src_category).order_by('id')
                for src_test in src_tests:
                    new_test = Test(category=new_category, name=src_test.name, purpose=src_test.purpose,
                                    procedure=src_test.procedure, expected=src_test.expected,
                                    created_by=request.user, created_at=datetime.now(),
                                    updated_by=request.user, updated_at=datetime.now(),
                                    redmine_wiki=src_test.redmine_wiki)
                    new_test.save()

                    src_configs = TestConfig.objects.filter(test=src_test).order_by('id')
                    for src_config in src_configs:
                        new_config = TestConfig(name=src_config.name, lang=src_config.lang,
                                                test=new_test, config=src_config.config)
                        new_config.save()

                    src_images = TestImage.objects.filter(test=src_test).order_by('id')
                    for src_image in src_images:
                        new_image = TestImage(name=src_image.name, image=src_image.image,
                                              test=new_test, width=src_image.width, height=src_image.height)
                        new_image.save()

                    src_files = TestFile.objects.filter(test=src_test).order_by('id')
                    for src_file in src_files:
                        new_file = TestFile(name=src_file.name, test=new_test, file=src_file.file)
                        new_file.save()

                    src_checklists = TestChecklist.objects.filter(test=src_test).order_by('id')
                    for src_checklist in src_checklists:
                        new_checklist = TestChecklist(name=src_checklist.name, test=new_test)
                        new_checklist.save()
                        src_checklist_items = TestChecklistItem.objects.filter(checklist=src_checklist).order_by('id')
                        for src_checklist_item in src_checklist_items:
                            new_checklist_item = TestChecklistItem(name=src_checklist_item.name,
                                                                   checklist=new_checklist)
                            new_checklist_item.save()

                    src_links = TestLink.objects.filter(test=src_test).order_by('id')
                    for src_link in src_links:
                        new_link = TestLink(name=src_link.name, test=new_test, url=src_link.url)
                        new_link.save()

                    src_comments = TestComment.objects.filter(test=src_test).order_by('id')
                    for src_comment in src_comments:
                        new_comment = TestComment(name=src_comment.name, test=new_test, text=src_comment.text)
                        new_comment.save()

            return HttpResponseRedirect(reverse('testplans', kwargs={'tab_id': 1}))
    else:
        testplan = get_object_or_404(Testplan, id=pk)
        form = TestplanForm(initial={'name': testplan.name,
                                     'version': testplan.version,
                                     'device_type': testplan.device_type.id,
                                     'created_by': request.user,
                                     'created_at': datetime.now(),
                                     'updated_by': request.user,
                                     'updated_at': datetime.now(),
                                     'redmine_parent': testplan.redmine_parent,
                                     'redmine_project': testplan.redmine_project})
        return render(request, 'testplan/clone.html', {'form': form, 'tp_id': testplan.id})


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
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('tp_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.kwargs.get('tp_id'), 'tab_id': 3})
        return context

    def get_success_url(self):
        self.object.testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class CategoryDelete(DeleteView):
    model = Category
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        self.object.testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'testplan/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        self.object.testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestCreate(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'category': self.kwargs.get('category_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        context['back_url'] = reverse('testplan_details', kwargs={'pk': category.testplan.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        self.object.category.testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.category.testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestDelete(DeleteView):
    model = Test
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        testplan = self.object.category.testplan
        testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestUpdate(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        self.object.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@login_required
def test_details(request, pk, tab_id):
    test = get_object_or_404(Test, id=pk)
    testplan = test.category.testplan
    procedure = textile.textile(test.procedure)
    expected = textile.textile(test.expected)
    configs = TestConfig.objects.filter(test=test).order_by('id')
    images = TestImage.objects.filter(test=test).order_by('id')
    files = TestFile.objects.filter(test=test).order_by('id')
    checklists = TestChecklist.objects.filter(test=test).order_by('id')
    int_values = TestIntegerValue.objects.filter(test=test).order_by('id')
    worksheets_count = checklists.count() + int_values.count()

    links = TestLink.objects.filter(test=test).order_by('id')
    comments = TestComment.objects.filter(test=test).order_by('id')
    for comment in comments:
        comment.text = textile.textile(comment.text)
    redmine_form = RedmineTestForm(initial={'project': testplan.redmine_project,
                                            'wiki': test.redmine_wiki, 'name': True, 'purpose': True,
                                            'procedure': True, 'expected': True, 'configs': True,
                                            'images': False, 'files': False, 'checklists': True,
                                            'links': True, 'comments': True})

    return render(request, 'testplan/test_details.html', {'tab_id': tab_id, 'testplan': testplan, 'test': test,
                                                          'procedure': procedure, 'expected': expected,
                                                          'configs': configs, 'images': images, 'files': files,
                                                          'checklists': checklists, 'int_values': int_values,
                                                          'worksheets_count': worksheets_count, 'links': links,
                                                          'comments': comments, 'redmine_form': redmine_form,
                                                          'redmine_url': settings.REDMINE_URL})


@method_decorator(login_required, name='dispatch')
class ChapterCreate(CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('tp_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.kwargs.get('tp_id'), 'tab_id': 2})
        return context

    def get_success_url(self):
        self.object.testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ChapterDelete(DeleteView):
    model = Chapter
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('chapter_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        self.object.testplan.update_timestamp(user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class ChapterUpdate(UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'testplan/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('chapter_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        self.object.testplan.update_timestamp(user=self.request.user)
        return reverse('chapter_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@login_required
def chapter_details(request, pk, tab_id):
    chapter = get_object_or_404(Chapter, id=pk)
    if chapter.text:
        chapter_text = textile.textile(chapter.text)
    else:
        chapter_text = chapter.text

    redmine_chapter_form = RedmineChapterForm(initial={'project': chapter.testplan.redmine_project,
                                                       'wiki': chapter.redmine_wiki})
    redmine_url = settings.REDMINE_URL
    return render(request, 'testplan/chapter_details.html', {'chapter': chapter, 'testplan': chapter.testplan,
                                                             'chapter_text': chapter_text,
                                                             'redmine_form': redmine_chapter_form,
                                                             'redmine_url': redmine_url, 'tab_id': tab_id})


@login_required
def clear_chapters(request, tp_id):
    testplan = get_object_or_404(Testplan, id=tp_id)
    if request.method == 'POST':
        Chapter.objects.filter(testplan=testplan).delete()
        testplan.update_timestamp(user=request.user)
        return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': tp_id, 'tab_id': 2}))
    else:
        back_url = reverse('testplan_details', kwargs={'pk': tp_id, 'tab_id': 2})
        message = _('Are you sure you want to clear chapters for "') + testplan.name + '"?'
        return render(request, 'testplan/clear.html', {'testplan': testplan, 'back_url': back_url, 'message': message})


@login_required
def clear_tests(request, tp_id):
    testplan = get_object_or_404(Testplan, id=tp_id)
    if request.method == 'POST':
        Category.objects.filter(testplan=testplan).delete()
        testplan.update_timestamp(user=request.user)
        return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': tp_id, 'tab_id': 3}))
    else:
        back_url = reverse('testplan_details', kwargs={'pk': tp_id, 'tab_id': 3})
        message = _('Are you sure you want to clear tests for "') + testplan.name + '"?'
        return render(request, 'testplan/clear.html', {'testplan': testplan, 'back_url': back_url, 'message': message})


@method_decorator(login_required, name='dispatch')
class TestConfigCreate(CreateView):
    model = TestConfig
    form_class = TestConfigForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 5})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class TestConfigDelete(DeleteView):
    model = TestConfig
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class TestConfigUpdate(UpdateView):
    model = TestConfig
    form_class = TestConfigForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class TestImageCreate(CreateView):
    model = TestImage
    form_class = TestImageForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestImageDelete(DeleteView):
    model = TestImage
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestImageUpdate(UpdateView):
    model = TestImage
    form_class = TestImageForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestFileCreate(CreateView):
    model = TestFile
    form_class = TestFileForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 7})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class TestFileDelete(DeleteView):
    model = TestFile
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class TestFileUpdate(UpdateView):
    model = TestFile
    form_class = TestFileForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class TestChecklistCreate(CreateView):
    model = TestChecklist
    form_class = TestChecklistForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestChecklistDelete(DeleteView):
    model = TestChecklist
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestChecklistUpdate(UpdateView):
    model = TestChecklist
    form_class = TestChecklistForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestChecklistItemCreate(CreateView):
    model = TestChecklistItem
    form_class = TestChecklistItemForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'checklist': self.kwargs.get('checklist_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklist = get_object_or_404(TestChecklist, id=self.kwargs.get('checklist_id'))
        context['back_url'] = reverse('test_details', kwargs={'pk': checklist.test.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.checklist.test.update_timestamp(user=self.request.user)
        self.object.checklist.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.checklist.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestChecklistItemDelete(DeleteView):
    model = TestChecklistItem
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.checklist.test.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.checklist.test.update_timestamp(user=self.request.user)
        self.object.checklist.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.checklist.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestChecklistItemUpdate(UpdateView):
    model = TestChecklistItem
    form_class = TestChecklistItemForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'checklist_id': self.kwargs.get('checklist_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.checklist.test.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.checklist.test.update_timestamp(user=self.request.user)
        self.object.checklist.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.checklist.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestIntegerValueCreate(CreateView):
    model = TestIntegerValue
    form_class = TestIntegerValueForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestIntegerValueDelete(DeleteView):
    model = TestIntegerValue
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestIntegerValueUpdate(UpdateView):
    model = TestIntegerValue
    form_class = TestIntegerValueForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 8})


@method_decorator(login_required, name='dispatch')
class TestLinkCreate(CreateView):
    model = TestLink
    form_class = TestLinkForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 9})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 9})


@method_decorator(login_required, name='dispatch')
class TestLinkDelete(DeleteView):
    model = TestLink
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 9})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 9})


@method_decorator(login_required, name='dispatch')
class TestLinkUpdate(UpdateView):
    model = TestLink
    form_class = TestLinkForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 9})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 9})


@method_decorator(login_required, name='dispatch')
class TestCommentCreate(CreateView):
    model = TestComment
    form_class = TestCommentForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 10})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 10})


@method_decorator(login_required, name='dispatch')
class TestCommentDelete(DeleteView):
    model = TestComment
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 10})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 10})


@method_decorator(login_required, name='dispatch')
class TestCommentUpdate(UpdateView):
    model = TestComment
    form_class = TestCommentForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'test_id': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 10})
        return context

    def get_success_url(self):
        self.object.test.update_timestamp(user=self.request.user)
        self.object.test.category.testplan.update_timestamp(user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 10})


@method_decorator(login_required, name='dispatch')
class PatternCreate(CreateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_success_url(self):
        return reverse('pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class PatternDelete(DeleteView):
    model = Pattern
    template_name = 'testplan/delete.html'

    def get_success_url(self):
        return reverse('testplans', kwargs={'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class PatternUpdate(UpdateView):
    model = Pattern
    form_class = PatternForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_success_url(self):
        pattern = get_object_or_404(Pattern, id=self.object.id)
        pattern.update_timestamp(user=self.request.user)
        return reverse('pattern_details', kwargs={'pk': pattern.id, 'tab_id': 1})
