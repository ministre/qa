from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from device.models import DeviceType
from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceAttrError


@login_required
def redmine_testplan_import(request):
    if request.method == 'POST':
        pass
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
