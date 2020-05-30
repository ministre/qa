from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RedmineProject, RedmineTest, RedmineTestPlan
from testplan.models import Test, TestConfig, TestImage, TestFile, TestChecklist, TestLink, TestComment, Testplan, \
    Chapter, Category
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404
from django.urls import reverse


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
            return render(request, 'redmine/result.html', {'message': is_project[1], 'back_url': back_url})

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
            message = 'Data imported successfully'
        else:
            message = test_details[1]
        return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})

    else:
        message = 'Page not found'
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

        wiki_page = RedmineTest().export(project=request.POST['project'], wiki_title=request.POST['wiki'], name=name,
                                         purpose=purpose, procedure=procedure, configs=configs, images=images,
                                         files=files, expected=expected, checklists=checklists, links=links,
                                         comments=comments)[1]
        return render(request, 'redmine/result.html', {'message': wiki_page, 'back_url': back_url})
    else:
        message = 'Page not found'
        back_url = reverse('testplans', kwargs={'tab_id': 1})
    return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})


@login_required
def import_testplan(request):
    pass


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

        r = RedmineTestPlan().export(project=request.POST['project'], project_name=testplan.name,
                                     parent=request.POST['parent'], version=testplan.version,
                                     chapters=chapters, categories=categories)

        message = 'Success'
        return render(request, 'redmine/result.html', {'message': message, 'back_url': back_url})

    else:
        message = 'Page not found'
        return render(request, 'redmine/result.html', {'message': message,
                                                       'back_url': reverse('testplans', kwargs={'tab_id': 1})})
