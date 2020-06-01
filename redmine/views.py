from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RedmineProject, RedmineChapter, RedmineTest, RedmineTestplan
from testplan.models import Test, TestConfig, TestImage, TestFile, TestChecklist, TestChecklistItem, TestLink, \
    TestComment, Testplan, Chapter, Category
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from datetime import datetime


@login_required
def export_chapter(request):
    if request.method == "POST":
        chapter = get_object_or_404(Chapter, id=request.POST['chapter'])
        back_url = reverse('chapter_details', kwargs={'pk': chapter.id, 'tab_id': 3})
        # check project
        project = request.POST['project']
        is_project = RedmineProject().check_project(project=project)
        if not is_project[0]:
            return render(request, 'redmine/result.html', {'message': is_project, 'back_url': back_url})
        message = RedmineChapter().export(project=project, wiki_title=request.POST['wiki'], chapter=chapter)
    else:
        message = [False, 'Page not found']
        back_url = reverse('testplans', kwargs={'tab_id': 1})
    return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})


@login_required
def import_chapter(request):
    if request.method == "POST":
        chapter = get_object_or_404(Chapter, id=request.POST['chapter'])
        back_url = reverse('chapter_details', kwargs={'pk': chapter.id, 'tab_id': 3})
        # check project
        project = request.POST['project']
        is_project = RedmineProject().check_project(project=project)
        if not is_project[0]:
            return render(request, 'redmine/result.html', {'message': is_project, 'back_url': back_url})
        # parse chapter
        parse_details = RedmineChapter().parse_details(project=project, wiki_title=request.POST['wiki'])
        if parse_details[0]:
            message = chapter.update_details(name=parse_details[1]['name'], text=parse_details[1]['text'],
                                             user=request.user)
        else:
            message = parse_details
    else:
        message = [False, 'Page not found']
        back_url = reverse('testplans', kwargs={'tab_id': 1})
    return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})


@login_required
def export_test(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test'])
        back_url = reverse('test_details', kwargs={'pk': test.id, 'tab_id': 11})
        # collect data
        name = test.name
        try:
            if request.POST['purpose']:
                purpose = test.purpose
            else:
                purpose = None
        except MultiValueDictKeyError:
            purpose = None
        try:
            if request.POST['procedure']:
                procedure = test.procedure
            else:
                procedure = None
        except MultiValueDictKeyError:
            procedure = None
        try:
            if request.POST['configs']:
                configs = TestConfig.objects.filter(test=test).order_by('id')
            else:
                configs = None
        except MultiValueDictKeyError:
            configs = None
        try:
            if request.POST['images']:
                images = TestImage.objects.filter(test=test).order_by('id')
            else:
                images = None
        except MultiValueDictKeyError:
            images = None
        try:
            if request.POST['files']:
                files = TestFile.objects.filter(test=test).order_by('id')
            else:
                files = None
        except MultiValueDictKeyError:
            files = None
        try:
            if request.POST['expected']:
                expected = test.expected
            else:
                expected = None
        except MultiValueDictKeyError:
            expected = None
        try:
            if request.POST['checklists']:
                checklists = TestChecklist.objects.filter(test=test).order_by('id')
            else:
                checklists = None
        except MultiValueDictKeyError:
            checklists = None
        try:
            if request.POST['links']:
                links = TestLink.objects.filter(test=test).order_by('id')
            else:
                links = None
        except MultiValueDictKeyError:
            links = None
        try:
            if request.POST['comments']:
                comments = TestComment.objects.filter(test=test).order_by('id')
            else:
                comments = None
        except MultiValueDictKeyError:
            comments = None

        # check project
        project = request.POST['project']
        is_project = RedmineProject().check_project(project=project)
        if not is_project[0]:
            return render(request, 'redmine/result.html', {'message': is_project[1], 'back_url': back_url})

        message = RedmineTest().export(project=request.POST['project'], wiki_title=request.POST['wiki'], name=name,
                                       purpose=purpose, procedure=procedure, configs=configs, images=images,
                                       files=files, expected=expected, checklists=checklists, links=links,
                                       comments=comments)
    else:
        message = [False, 'Page not found']
        back_url = reverse('testplans', kwargs={'tab_id': 1})
    return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})


@login_required
def import_test(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test'])
        back_url = reverse('test_details', kwargs={'pk': test.id, 'tab_id': 11})
        # collect data
        try:
            if request.POST['purpose']:
                purpose = True
            else:
                purpose = False
        except MultiValueDictKeyError:
            purpose = False
        try:
            if request.POST['procedure']:
                procedure = True
            else:
                procedure = False
        except MultiValueDictKeyError:
            procedure = False
        try:
            if request.POST['configs']:
                configs = True
            else:
                configs = False
        except MultiValueDictKeyError:
            configs = False
        try:
            if request.POST['images']:
                images = True
            else:
                images = False
        except MultiValueDictKeyError:
            images = False
        try:
            if request.POST['files']:
                files = True
            else:
                files = False
        except MultiValueDictKeyError:
            files = False
        try:
            if request.POST['expected']:
                expected = True
            else:
                expected = False
        except MultiValueDictKeyError:
            expected = False
        try:
            if request.POST['checklists']:
                checklists = True
            else:
                checklists = False
        except MultiValueDictKeyError:
            checklists = False
        try:
            if request.POST['links']:
                links = True
            else:
                links = False
        except MultiValueDictKeyError:
            links = False
        try:
            if request.POST['comments']:
                comments = True
            else:
                comments = False
        except MultiValueDictKeyError:
            comments = False

        # check project
        project = request.POST['project']
        is_project = RedmineProject().check_project(project=project)
        if not is_project[0]:
            return render(request, 'redmine/result.html', {'message': is_project, 'back_url': back_url})

        test_details = RedmineTest().parse_details(project=project, wiki_title=request.POST['wiki'],
                                                   is_purpose=purpose, is_procedure=procedure, is_configs=configs,
                                                   is_images=images, is_files=files, is_expected=expected,
                                                   is_checklists=checklists, is_links=links, is_comments=comments)
        if test_details[0]:
            test.update_details(name=test_details[1]['name'],
                                purpose=test_details[1]['purpose'],
                                procedure=test_details[1]['procedure'],
                                expected=test_details[1]['expected'],
                                clear_configs=configs,
                                configs=test_details[1]['configs'],
                                images=test_details[1]['images'],
                                files=test_details[1]['files'],
                                clear_checklists=checklists,
                                checklists=test_details[1]['checklists'],
                                clear_links=links,
                                links=test_details[1]['links'],
                                clear_comments=comments,
                                comments=test_details[1]['comments'])
            test.update_timestamp(request.user)
            message = [True, 'Data has been updated']
        else:
            message = test_details
    else:
        message = [False, 'Page not found']
        back_url = reverse('testplans', kwargs={'tab_id': 1})
    return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})


@login_required
def export_testplan(request):
    if request.method == "POST":
        testplan = get_object_or_404(Testplan, id=request.POST['testplan'])
        back_url = reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 5})
        # collect data
        try:
            if request.POST['chapters']:
                chapters = Chapter.objects.filter(testplan=testplan).order_by('id')
            else:
                chapters = None
        except MultiValueDictKeyError:
            chapters = None
        try:
            if request.POST['tests']:
                categories = Category.objects.filter(testplan=testplan).order_by('id')
            else:
                categories = None
        except MultiValueDictKeyError:
            categories = None

        message = RedmineTestplan().export(project=request.POST['project'], project_name=testplan.name,
                                           parent=request.POST['parent'], version=testplan.version,
                                           chapters=chapters, categories=categories)
    else:
        message = [False, 'Page not found']
        back_url = reverse('testplans', kwargs={'tab_id': 1})
    return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})


@login_required
def import_testplan(request):
    if request.method == "POST":
        testplan = get_object_or_404(Testplan, id=request.POST['testplan'])
        back_url = reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 5})
        # check project
        project = request.POST['project']
        is_project = RedmineProject().check_project(project=project)
        if not is_project[0]:
            return render(request, 'redmine/result.html', {'message': is_project, 'back_url': back_url})
        # collect attributes
        try:
            is_chapters = request.POST['chapters']
        except MultiValueDictKeyError:
            is_chapters = None
        try:
            is_tests = request.POST['tests']
        except MultiValueDictKeyError:
            is_tests = None
        # parse data
        testplan_details = RedmineTestplan().parse_details(project=project, is_chapters=is_chapters, is_tests=is_tests)
        # update data
        if testplan_details[0]:
            if is_chapters:
                chapters = testplan_details[1]['chapters']
                for chapter in chapters:
                    Chapter.objects.update_or_create(testplan=testplan, name=chapter['name'],
                                                     defaults={'testplan': testplan,
                                                               'name': chapter['name'],
                                                               'text': chapter['text'],
                                                               'redmine_wiki': chapter['redmine_wiki'],
                                                               'created_by': request.user,
                                                               'updated_by': request.user,
                                                               'updated_at': datetime.now})
            if is_tests:
                categories = testplan_details[1]['categories']
                for category in categories:
                    cat, created = Category.objects.update_or_create(testplan=testplan, name=category['name'],
                                                                     defaults={'testplan': testplan,
                                                                               'name': category['name']})
                    tests = category['tests']
                    for test in tests:
                        t, created = Test.objects.update_or_create(category=cat, name=test['name'],
                                                                   defaults={'category': cat,
                                                                             'name': test['name'],
                                                                             'purpose': test['purpose'],
                                                                             'procedure': test['procedure'],
                                                                             'expected': test['expected'],
                                                                             'created_by': request.user,
                                                                             'updated_by': request.user,
                                                                             'updated_at': datetime.now,
                                                                             'redmine_wiki': test['redmine_wiki']})
                        configs = test['configs']
                        if configs:
                            for config in configs:
                                TestConfig.objects.update_or_create(test=t, name=config[0],
                                                                    defaults={'test': t,
                                                                              'name': config[0],
                                                                              'lang': config[1],
                                                                              'config': config[2]})
                        images = test['images']
                        if images:
                            pass
                        files = test['files']
                        if files:
                            pass
                        checklists = test['checklists']
                        if checklists:
                            for checklist in checklists:
                                ch, cr = TestChecklist.objects.update_or_create(test=t, name=checklist['name'],
                                                                                defaults={'test': t,
                                                                                          'name': checklist['name']})
                                items = checklist['items']
                                if items:
                                    for item in items:
                                        TestChecklistItem.objects.update_or_create(checklist=ch, name=item,
                                                                                   defaults={'checklist': ch,
                                                                                             'name': item})
                        links = test['links']
                        if links:
                            for link in links:
                                TestLink.objects.update_or_create(test=t, name=link[0],
                                                                  defaults={'test': t, 'name': link[0], 'url': link[1]})
                        comments = test['comments']
                        if comments:
                            for comment in comments:
                                TestComment.objects.update_or_create(test=t, name=comment[0],
                                                                     defaults={'test': t, 'name': comment[0],
                                                                               'text': comment[1]})
            message = testplan_details
        else:
            return testplan_details
    else:
        message = [False, 'Page not found']
        back_url = reverse('testplans', kwargs={'tab_id': 1})
    return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})
