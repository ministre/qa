from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from device.models import DeviceType
from testplan.models import Testplan, TestplanCategory, Test
from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceAttrError, ResourceNotFoundError
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import re


def redmine_connect():
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.0.4')
    return redmine


@login_required
def import_testplan(request):
    if request.method == 'POST':
        testplan_project = request.POST['testplan_project']
        tag = request.POST['tag']
        # create testplan
        try:
            testplan_id = create_testplan(testplan_project, tag, request.user)
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})
        # create tests
        redmine_url = '/projects/' + testplan_project + '/wiki'
        tests_create_from_wiki(testplan_id, redmine_url, tag)

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
            if re.search(tag+'\)', block):
                blocks[i] = blocks[i].replace('\n{{collapse(#'+tag+')', '')
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
def create_testplan(testplan_project, tag, created_by):
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)
    try:
        wiki_page = redmine.wiki_page.get('Headers', project_id=testplan_project)
    except ResourceNotFoundError:
        raise ValueError('[create_testplan]: Headers wiki page not found')

    ctx = collapse_filter(wiki_page.text, tag)
    head = parse_testplan_head(ctx)
    new_testplan = Testplan(name=head['title'],
                            version=head['version'],
                            device_type=DeviceType.objects.get(tag=tag),
                            redmine_url='/projects/' + testplan_project + '/wiki',
                            created_by=created_by)
    new_testplan.save()
    return new_testplan.id


@login_required
def test_details_update(request):
    if request.method == "POST":
        test_id = request.POST['test_id']
        redmine_url = request.POST['redmine_url']
        tag = request.POST['tag']
        try:
            test_details_update_from_wiki(test_id, redmine_url, tag)
            return HttpResponseRedirect('/testplan/test/' + test_id + '/')
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})


# Update test details from Redmine wiki page
def test_details_update_from_wiki(test_id, redmine_url, tag):
    if not redmine_url:
        raise ValueError('Test #'+str(test_id)+': Import error - REDMINE_URL not found')
    try:
        test = Test.objects.get(id=test_id)
    except ObjectDoesNotExist:
        raise ValueError('Test #'+str(test_id)+': Import error - Test object not found')

    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)

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
    test.procedure = collapse_filter(wiki_blocks[2], tag).replace("Процедура\r\n\r\n", "")
    test.expected = collapse_filter(wiki_blocks[3], tag).replace("Ожидаемый результат\r\n\r\n", "")
    test.redmine_url = redmine_url
    test.save()
    return test.id


@login_required
def tests_import(request):
    if request.method == "POST":
        testplan_id = request.POST['testplan_id']
        redmine_url = request.POST['redmine_url']
        tag = request.POST['tag']
        try:
            tests_create_from_wiki(testplan_id, redmine_url, tag)
            return HttpResponseRedirect('/testplan/' + str(testplan_id) + '/')
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})
    else:
        return HttpResponseRedirect('/testplan/')


# Import all tests from Redmine wiki page
def tests_create_from_wiki(testplan_id, redmine_url, tag):
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)
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
            category = TestplanCategory.objects.get(Q(testplan=Testplan.objects.get(id=testplan_id)) &
                                                    Q(name=item.category)).id
            test_redmine_url = redmine_url + '/' + item.keyword
            new_test = Test.objects.create(category=TestplanCategory.objects.get(id=category),
                                           name=item.name,
                                           redmine_url=test_redmine_url)
            test_details_update_from_wiki(new_test.id, test_redmine_url, tag)

        except ObjectDoesNotExist:
            # create category if not found
            new_category = TestplanCategory.objects.create(name=item.category,
                                                           testplan=Testplan.objects.get(id=testplan_id))
            test_redmine_url = redmine_url + '/' + item.keyword
            new_test = Test.objects.create(category=TestplanCategory.objects.get(id=new_category.id),
                                           name=item.name,
                                           redmine_url=test_redmine_url)
            test_details_update_from_wiki(new_test.id, test_redmine_url, tag)
    return len(items)
