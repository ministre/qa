from django.shortcuts import render
from django.shortcuts import get_object_or_404
from testplan.models import Testplan
from docx import Document
import os
from django.conf import settings
from django.http import HttpResponse, Http404


# Create your views here.
def build_testplan(request):
    if request.method == 'POST':
        testplan = get_object_or_404(Testplan, id=request.POST['testplan'])
        document = Document()
        document.add_paragraph('Test', style='TOCHeading')

        testplan_filename = settings.MEDIA_ROOT + '/testplan_' + str(testplan.id) + '.docx'
        document.save(testplan_filename)

        file_path = os.path.join(settings.MEDIA_ROOT, testplan_filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
