from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from device.models import DeviceType, Device
from testplan.models import Testplan, Category, Test, Chapter, TestConfig, Pattern
from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceAttrError, ResourceNotFoundError
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import re
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import RedmineProject
from django.urls import reverse


def redmine_connect():
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.0.4')
    return redmine


@login_required
def import_testplan(request):
    if request.method == 'POST':
        project = request.POST['project']
        tag = request.POST['tag']
        # create testplan
        try:
            testplan_id = create_testplan(project, tag, request.user)
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})
        # create tests
        redmine_url = '/projects/' + project + '/wiki'
        tests_create_from_wiki(testplan_id, redmine_url, tag, request.user)
        # create chapters
        chapters_create_from_wiki(testplan_id, redmine_url, tag, request.user)
        return HttpResponseRedirect('/testplan/')
    else:
        redmine = redmine_connect()
        projects = []
        for project in redmine.project.all():
            try:
                if project.parent.name == settings.REDMINE_TESTPLAN_PROJECTNAME:
                    projects.append(project)
            except ResourceAttrError:
                pass
        tags = DeviceType.objects.all().order_by("tag")
        return render(request, 'redmine/import_testplan.html', {'tags': tags, 'projects': projects})


# Extract spoilers of device-type from wiki page
def collapse_filter(ctx, tag):
    blocks = ctx.split('}}')
    for i, block in enumerate(blocks):
        if re.search('{{collapse\(#', block):
            if re.search(tag + '\)', block):
                blocks[i] = blocks[i].replace('\n{{collapse(#' + tag + ')', '')
            else:
                blocks[i] = ''
    ctx = ''.join(blocks)
    return ctx


def parse_testplan_head(ctx):
    head = dict()
    blocks = ctx.split('|')
    head['title'] = blocks[2].strip()
    head['version'] = blocks[5].strip()
    return head


class Item:
    def __init__(self, category, keyword, name):
        self.category = category
        self.keyword = keyword
        self.name = name


# Parse tests from Redmine wiki page
def item_filter(ctx, tag):
    items = []
    blocks = ctx.split('h2')
    for i, block in enumerate(blocks):
        # peek categories
        if block.startswith('. '):
            s = blocks[i].index('\n')
            category = blocks[i][2:s-1]
            # peek items
            sblocks = blocks[i].split('*')
            for j, sblock in enumerate(sblocks):
                # check tags
                if (('\nall' in sblocks[j]) and ('\n!'+tag not in sblocks[j])) or ('\n'+tag in sblocks[j]):
                    p = sblocks[j].index('|')
                    r = sblocks[j].index(']')
                    keyword = sblocks[j][3:p]
                    name = sblocks[j][p+1:r]
                    items.append(Item(category, keyword, name))
    return items


# Create new testplan from Redmine wiki page
def create_testplan(testplan_project, tag, user):
    redmine = redmine_connect()
    try:
        wiki_page = redmine.wiki_page.get('Headers', project_id=testplan_project)
    except ResourceNotFoundError:
        raise ValueError('[create_testplan]: Headers wiki page not found')

    ctx = collapse_filter(wiki_page.text, tag)
    head = parse_testplan_head(ctx)
    new_testplan = Testplan(name=head['title'], version=head['version'], device_type=DeviceType.objects.get(tag=tag),
                            redmine_url='/projects/' + testplan_project + '/wiki', created_by=user,
                            created_at=datetime.now(), updated_by=user, updated_at=datetime.now())
    new_testplan.save()
    return new_testplan.id


@login_required
def import_p_test_details(request):
    if request.method == "POST":
        test_id = request.POST['test_id']
        testplan_id = request.POST['testplan_id']
        redmine_url = request.POST['redmine_url']
        tag = request.POST['tag']
        try:
            test_details_update_from_wiki(test_id, redmine_url, tag, request.user)
            testplan = get_object_or_404(Testplan, id=testplan_id)
            testplan.update_timestamp(user=request.user)
            return HttpResponseRedirect('/testplan/' + testplan_id + '/test/' + test_id + '/')
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})


# Update test details from Redmine wiki page
def test_details_update_from_wiki(test_id, redmine_url, tag, user):
    if not redmine_url:
        raise ValueError('Test #'+str(test_id)+': Import error - REDMINE_URL not found')
    try:
        test = Test.objects.get(id=test_id)
    except ObjectDoesNotExist:
        raise ValueError('Test #'+str(test_id)+': Import error - Test object not found')

    redmine = redmine_connect()

    try:
        project_id = redmine_url.split('/')[2]
        wiki_id = redmine_url.split('/')[4]
    except IndexError:
        raise ValueError('Test #'+str(test_id)+': Import error - Can not parse project_id or wiki_id from REDMINE_URL')

    try:
        wiki_page = redmine.wiki_page.get(wiki_id, project_id=project_id)
    except ResourceNotFoundError:
        raise ValueError('Test #'+str(test_id)+': Import error - Wiki page ' +
                         settings.REDMINE_URL + redmine_url + ' not found')
    wiki_blocks = wiki_page.text.split('\nh2. ')
    test.name = wiki_blocks[0].split('h1. ')[1][0:-3]
    test.purpose = wiki_blocks[1].split('\r\n')[2]

    procedure = collapse_filter(wiki_blocks[2], tag).replace("Процедура\r\n\r\n", "")
    # parse test configs
    configs = pick_up_test_config(procedure)
    for config in configs:
        new_test_config = TestConfig(test=test, name=config['name'], lang=config['style'], config=config['config'])
        new_test_config.save()
    # cut test configs
    test.procedure = cut_test_config(procedure)

    test.expected = collapse_filter(wiki_blocks[3], tag).replace("Ожидаемый результат\r\n\r\n", "")
    test.redmine_url = redmine_url
    test.updated_by = user
    test.updated_at = datetime.now()
    test.save()

    return test.id


def pick_up_test_config(ctx):
    configs = []
    blocks = ctx.split('\n</code></pre>\r')
    for block in blocks:
        if re.search('\n<pre><code class="', block):
            # config style
            s_block = block.split('\n<pre><code class="')[1]
            style = s_block.split('">\r')[0]
            # config
            s_block = block.split('">\r\n')[1]
            config = s_block.split('\n</code></pre>')[0]
            # config description
            name = None
            if re.search('\n> ', block):
                s_block = block.split('\n> ')[1]
                name = s_block.split('\r\n\r')[0]
            config = {'name': name, 'style': style, 'config': config}
            configs.append(config)
    return configs


def cut_test_config(ctx):
    blocks = ctx.split('\n</code></pre>\r')
    for i, block in enumerate(blocks):
        if re.search('\n<pre><code class="', block):
            if re.search('\n> ', block):
                cut_text = block.split('\n> ')
                blocks[i] = block.replace('\n> ' + cut_text[1], '')
            else:
                cut_text = block.split('\n<pre>')
                blocks[i] = block.replace('\n<pre>' + cut_text[1], '')
    ctx = ''.join(blocks)
    return ctx


@login_required
def import_all_tests(request):
    if request.method == "POST":
        testplan_id = request.POST['testplan_id']
        redmine_url = request.POST['redmine_url']
        tag = request.POST['tag']
        try:
            tests_create_from_wiki(testplan_id, redmine_url, tag, request.user)
            testplan = get_object_or_404(Testplan, id=testplan_id)
            testplan.update_timestamp(user=request.user)
            return HttpResponseRedirect('/testplan/' + str(testplan_id) + '/')
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})
    else:
        return HttpResponseRedirect('/testplan/')


# Import all tests from Redmine wiki page
def tests_create_from_wiki(testplan_id, redmine_url, tag, user):
    redmine = redmine_connect()
    if not redmine_url:
        raise ValueError("[tests_create_from_wiki]: value <redmine_url> not set in testplan #"
                         + str(testplan_id))
    try:
        project_id = redmine_url.split('/')[2]
    except IndexError:
        raise ValueError("[tests_create_from_wiki]: Can't parse <project_id> from <redmine_url> in testplan #"
                         + str(testplan_id))
    try:
        wiki_page = redmine.wiki_page.get('wiki', project_id=project_id)
    except ResourceNotFoundError:
        raise ValueError("[tests_create_from_wiki]: Wiki page " + settings.REDMINE_URL + redmine_url + " not found")

    items = item_filter(wiki_page.text, tag)
    for item in items:
        try:
            category = Category.objects.get(Q(testplan=Testplan.objects.get(id=testplan_id)) &
                                            Q(name=item.category)).id
            test_redmine_url = redmine_url + '/' + item.keyword
            new_test = Test.objects.create(category=Category.objects.get(id=category), name=item.name,
                                           redmine_url=test_redmine_url, created_by=user, updated_by=user)
            test_details_update_from_wiki(new_test.id, test_redmine_url, tag, user)

        except ObjectDoesNotExist:
            # create category if not found
            new_category = Category.objects.create(name=item.category, testplan=Testplan.objects.get(id=testplan_id))
            test_redmine_url = redmine_url + '/' + item.keyword
            new_test = Test.objects.create(category=Category.objects.get(id=new_category.id), name=item.name,
                                           redmine_url=test_redmine_url, created_by=user, updated_by=user)
            test_details_update_from_wiki(new_test.id, test_redmine_url, tag, user)
    return len(items)


@login_required
def import_all_chapters(request):
    if request.method == "POST":
        testplan_id = request.POST['testplan_id']
        redmine_url = request.POST['redmine_url']
        tag = request.POST['tag']
        try:
            chapters_create_from_wiki(testplan_id, redmine_url, tag, request.user)
            testplan = get_object_or_404(Testplan, id=testplan_id)
            testplan.update_timestamp(user=request.user)
            return HttpResponseRedirect('/testplan/' + str(testplan_id) + '/')
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})
    else:
        return HttpResponseRedirect('/testplan/')


# Import all chapters from Redmine wiki page
def chapters_create_from_wiki(testplan_id, redmine_url, tag, user):
    redmine = redmine_connect()
    if not redmine_url:
        raise ValueError("[chapters_create_from_wiki]: value <redmine_url> not set in testplan #"
                         + str(testplan_id))
    try:
        project_id = redmine_url.split('/')[2]
    except IndexError:
        raise ValueError("[chapters_create_from_wiki]: Can't parse <project_id> from <redmine_url> in testplan #"
                         + str(testplan_id))
    try:
        wiki_page = redmine.wiki_page.get('Sections', project_id=project_id)
    except ResourceNotFoundError:
        raise ValueError("[chapters_create_from_wiki]: Wiki page " + settings.REDMINE_URL + redmine_url + " not found")

    items = item_filter(wiki_page.text, tag)
    for item in items:
        chapter_redmine_url = redmine_url + '/' + item.keyword
        new_chapter = Chapter.objects.create(testplan=Testplan.objects.get(id=testplan_id), name=item.name,
                                             redmine_url=chapter_redmine_url, created_by=user, updated_by=user)
        chapter_details_update_from_wiki(new_chapter.id, chapter_redmine_url, tag, user)
    return len(items)


@login_required
def import_chapter_details(request):
    if request.method == "POST":
        chapter_id = request.POST['chapter_id']
        testplan_id = request.POST['testplan_id']
        redmine_url = request.POST['redmine_url']
        tag = request.POST['tag']
        try:
            chapter_details_update_from_wiki(chapter_id, redmine_url, tag, request.user)
            testplan = get_object_or_404(Testplan, id=testplan_id)
            testplan.update_timestamp(user=request.user)
            return HttpResponseRedirect('/testplan/' + testplan_id + '/chapter/' + chapter_id + '/')
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})


# Update chapter details from Redmine wiki page
def chapter_details_update_from_wiki(chapter_id, redmine_url, tag, user):
    if not redmine_url:
        raise ValueError('Chapter #'+str(chapter_id)+': Import error - REDMINE_URL not found')
    try:
        chapter = Chapter.objects.get(id=chapter_id)
    except ObjectDoesNotExist:
        raise ValueError('Chapter #'+str(chapter_id)+': Import error - Chapter object not found')
    redmine = redmine_connect()
    try:
        project_id = redmine_url.split('/')[2]
        wiki_id = redmine_url.split('/')[4]
    except IndexError:
        raise ValueError('Chapter #' + str(chapter_id) +
                         ': Import error - Can not parse project_id or wiki_id from REDMINE_URL')
    try:
        wiki_page = redmine.wiki_page.get(wiki_id, project_id=project_id)
    except ResourceNotFoundError:
        raise ValueError('Chapter #'+str(chapter_id)+': Import error - Wiki page ' +
                         settings.REDMINE_URL + redmine_url + ' not found')
    wiki_blocks = wiki_page.text.split('\r\n')
    chapter.name = wiki_blocks[0][4:]
    desc = '\r\n'.join(wiki_blocks[1:])
    chapter.text = collapse_filter(desc, tag)
    chapter.updated_by = user
    chapter.updated_at = datetime.now()
    chapter.save()
    return chapter.id


@login_required
def export_device_type(request):
    if request.method == "POST":
        device_type = get_object_or_404(DeviceType, id=request.POST['device_type'])
        r = RedmineProject(device_type.redmine_project).export_device_type(device_type)
        return render(request, 'redmine/device_type.html', {'message': r, 'device_type_id': device_type.id})
    else:
        return HttpResponseRedirect(reverse('device_types'))


@login_required
def export_device(request):
    if request.method == "POST":
        device = get_object_or_404(Device, id=request.POST['device'])
        r = RedmineProject(device.redmine_project).export_device(device)
        return render(request, 'redmine/device.html', {'message': r, 'device_id': device.id})
    else:
        return HttpResponseRedirect(reverse('devices'))


@login_required
def export_pattern(request):
    if request.method == "POST":
        pattern = get_object_or_404(Pattern, id=request.POST['pattern'])
        r = RedmineProject(pattern.redmine_project).export_pattern(pattern)
        return render(request, 'redmine/pattern.html', {'message': r, 'pattern_id': pattern.id})
    else:
        return HttpResponseRedirect(reverse('testplans', kwargs={'tab_id': 2}))


@login_required
def export_testplan(request):
    if request.method == "POST":
        testplan = get_object_or_404(Testplan, id=request.POST['testplan'])
        r = RedmineProject(testplan.redmine_project).export_testplan(testplan)
        return render(request, 'redmine/testplan.html', {'message': r, 'testplan_id': testplan.id})
    else:
        return HttpResponseRedirect(reverse('testplans', kwargs={'tab_id': 1}))


@login_required
def export_test(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test'])
        r = RedmineProject(test.category.testplan.redmine_project).export_test(test)
        return render(request, 'redmine/test.html', {'message': r, 'testplan_id': test.category.testplan.id,
                                                     'test_id': test.id})
    else:
        return HttpResponseRedirect(reverse('testplans', kwargs={'tab_id': 1}))
