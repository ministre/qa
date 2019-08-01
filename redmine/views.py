from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from device.models import DeviceType
from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceAttrError, ResourceNotFoundError
import re


@login_required
def redmine_testplan_import(request):
    if request.method == 'POST':
        testplan_project = request.POST['testplan_project']
        tag = request.POST['tag']
        redmine = Redmine(settings.REDMINE_URL, username=settings.REDMINE_USERNAME,
                          password=settings.REDMINE_PASSWORD)
        # get testplan title and version from wiki page
        try:
            wiki_page = redmine.wiki_page.get('Headers', project_id=testplan_project)
            ctx = collapse_filter(wiki_page.text, tag)
            return render(request, 'redmine/debug.html', {'ctx': ctx})

        except ResourceNotFoundError:
            message = "Redmine project or wiki page not found!"
            return render(request, 'redmine/error.html', {'message': message})
        ###
    else:
        redmine = Redmine(settings.REDMINE_URL, username=settings.REDMINE_USERNAME,
                          password=settings.REDMINE_PASSWORD)
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
    # ctx = tag
    return ctx
