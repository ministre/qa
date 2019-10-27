from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from device.models import DeviceType
from testplan.models import Testplan, TestplanCategory, Test
from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceAttrError, ResourceNotFoundError
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import re


@login_required
def testplan_import(request):
    if request.method == 'POST':
        testplan_project = request.POST['testplan_project']
        tag = request.POST['tag']
        # create testplan

        testplan_id = create_testplan(testplan_project, tag, request)
        if testplan_id:
            # create testplan categories
            if create_testplan_categories(testplan_id, testplan_project, tag):




                return HttpResponseRedirect('/testplan/')
                # return render(request, 'redmine/debug.html', {'message': testplan_id})

        else:
            message = "Can't parse wiki page - " + settings.REDMINE_URL + "/projects/" + \
                      testplan_project + "/wiki/Headers"
            return render(request, 'redmine/error.html', {'message': message})

    else:
        redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)
        testplan_projects = []
        for project in redmine.project.all():
            try:
                if project.parent.name == settings.REDMINE_TESTPLAN_PROJECTNAME:
                    testplan_projects.append(project)
            except ResourceAttrError:
                pass
        device_types_tags = DeviceType.objects.all().order_by("tag")
        return render(request, 'redmine/testplan_import.html', {'device_types_tags': device_types_tags,
                                                                'testplan_projects': testplan_projects})


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
        def __init__(self, category_name, item_keyword, item_name):
            self.category_name = category_name
            self.item_keyword = item_keyword
            self.item_name = item_name


def item_filter(ctx, tag):
    items = []
    blocks = ctx.split('h2')
    for i, block in enumerate(blocks):
        # peek categories
        if block.startswith('. '):
            s = blocks[i].index('\n')
            category_name = blocks[i][2:s-1]
            # peek items
            sblocks = blocks[i].split('*')
            for j, sblock in enumerate(sblocks):
                # check tags
                if (('\nall' in sblocks[j]) and ('\n!'+tag not in sblocks[j])) or ('\n'+tag in sblocks[j]):
                    p = sblocks[j].index('|')
                    r = sblocks[j].index(']')
                    item_keyword = sblocks[j][3:p]
                    item_name = sblocks[j][p+1:r]
                    items.append(Item(category_name, item_keyword, item_name))
    return items


def create_testplan(testplan_project, tag, request):
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)
    try:
        wiki_page = redmine.wiki_page.get('Headers', project_id=testplan_project)
        ctx = collapse_filter(wiki_page.text, tag)
        head = parse_testplan_head(ctx)
        new_testplan = Testplan(name=head['title'], version=head['version'],
                                device_type=DeviceType.objects.get(tag=tag),
                                redmine_url='/projects/' + testplan_project + '/wiki',
                                created_by=request.user)
        new_testplan.save()
        return new_testplan.id
    except ResourceNotFoundError:
        return


def create_testplan_categories(testplan_id, testplan_project, tag):
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)
    try:
        wiki_page = redmine.wiki_page.get('Wiki', project_id=testplan_project)
        ctx = wiki_page.text
        items = item_filter(ctx, tag)
        for item in items:
            new_category = TestplanCategory.objects.get_or_create(name=item.category_name,
                                                                  testplan=Testplan.objects.get(id=testplan_id))
            # new_category.save()
        return True

    except ResourceNotFoundError:
        return


@login_required
def test_details_update(request):
    if request.method == "POST":
        test_id = request.POST['test_id']
        redmine_url = request.POST['redmine_url']
        tag = request.POST['tag']
        try:
            debug = test_details_update_from_wiki(test_id, redmine_url, tag)
            return HttpResponseRedirect('/testplan/test/' + test_id + '/')
        except ValueError as e:
            return render(request, 'redmine/error.html', {'message': e})


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
        wiki_blocks = wiki_page.text.split('\nh2. ')
        test.name = wiki_blocks[0].split('h1. ')[1][0:-3]
        test.purpose = wiki_blocks[1].split('\r\n')[2]
        test.procedure = collapse_filter(wiki_blocks[2], tag).replace("Процедура\r\n\r\n", "")
        test.expected = collapse_filter(wiki_blocks[3], tag).replace("Ожидаемый результат\r\n\r\n", "")
        test.redmine_url = redmine_url
        test.save()
        return test.id

    except ResourceNotFoundError:
        raise ValueError('Test #'+str(test_id)+': Import error - Wiki page ' +
                         settings.REDMINE_URL + redmine_url + ' not found')


def test_create_from_wiki(testplan_id, redmine_url, tag):

#
#
#

    categories = TestplanCategory.objects.filter(testplan=testplan_id)
    for category in categories:
        pass
    pass