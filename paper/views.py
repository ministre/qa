from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from testplan.models import Testplan, Category, Test
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from docx import Document


@login_required
def make_testplan(request):
    if request.method == 'POST':
        testplan_id = request.POST['testplan_id']
        testplan = get_object_or_404(Testplan, id=testplan_id)
        categories = Category.objects.filter(testplan=testplan)

        document = Document()
        document.add_heading(testplan.name, 0)

        for category in categories:
            document.add_heading(category.name, level=1)

            tests = Test.objects.filter(category=category)
            for test in tests:
                document.add_heading(test.name, level=2)

                document.add_heading('Цель', level=3)
                p = document.add_paragraph(test.purpose)

                document.add_heading('Процедура', level=3)
                p = document.add_paragraph(test.procedure)

                document.add_heading('Ожидаемый результат', level=3)
                p = document.add_paragraph(test.expected)

        document.add_page_break()
        document.save('demo.docx')

        return HttpResponseRedirect('/testplan/' + testplan_id + '/')
    else:
        return HttpResponseRedirect('/testplan/')
