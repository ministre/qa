from django.shortcuts import render
from django.shortcuts import get_object_or_404
from testplan.models import Testplan, Category, Test
from docx import Document
from docx.shared import Pt, RGBColor
import os
from django.conf import settings
from django.http import HttpResponse, Http404


# Create your views here.
def build_testplan(request):
    if request.method == 'POST':
        testplan = get_object_or_404(Testplan, id=request.POST['testplan'])
        document = Document()

        style = document.styles['Heading 1']
        style.paragraph_format.space_before = Pt(5)
        style.font.size = Pt(16)
        style.font.color.rgb = RGBColor(0x77, 0x00, 0xff)

        document.add_paragraph('Test', style='TOCHeading')

        categories = Category.objects.filter(testplan=testplan).order_by('id')
        for i, category in enumerate(categories):
            document.add_heading(str(i+1) + '. ' + category.name, level=1)

            tests = Test.objects.filter(category=category).order_by('id')
            for j, test in enumerate(tests):
                document.add_heading(str(i+1) + '.' + str(j+1) + '. ' + test.name, level=2)

                # purpose
                document.add_paragraph('Цель', style='Body Text')
                document.add_paragraph(test.purpose, style='Body Text')

        testplan_filename = settings.MEDIA_ROOT + '/testplan_' + str(testplan.id) + '.docx'
        document.save(testplan_filename)

        file_path = os.path.join(settings.MEDIA_ROOT, testplan_filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
