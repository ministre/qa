from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


@login_required
def make_testplan(request):
    if request.method == 'POST':
        testplan_id = request.POST['testplan_id']
        return HttpResponseRedirect('/testplan/')
    else:
        return HttpResponseRedirect('/testplan/')
