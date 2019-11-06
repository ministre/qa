from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from testplan.models import Testplan, Category, Test
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from docx import Document
from docx.shared import Cm


@login_required
def make_testplan(request):
    if request.method == 'POST':
        testplan_id = request.POST['testplan_id']
        testplan = get_object_or_404(Testplan, id=testplan_id)
        categories = Category.objects.filter(testplan=testplan)

        document = Document()
        document.add_heading(testplan.name, 0)
        document.add_paragraph('Редакция: ' + testplan.version)
        document.add_page_break()

        section = document.sections
        section[0].left_margin = Cm(2.5)
        section[0].right_margin = Cm(1)
        section[0].top_margin = Cm(1)
        section[0].bottom_margin = Cm(1)

        for i, category in enumerate(categories):
            document.add_heading(str(i+1) + '. ' + category.name, level=1)

            tests = Test.objects.filter(category=category)
            for j, test in enumerate(tests):
                document.add_heading(str(i+1) + '.' + str(j+1) + '. ' + test.name, level=2)

                # test description
                table = document.add_table(rows=3, cols=2)

                table.style = 'Table Grid'

                table.allow_autofit = False
                for cell in table.columns[0].cells:
                    cell.width = Cm(2.5)
                for cell in table.columns[1].cells:
                    cell.width = Cm(15.5)

                table.cell(0, 0).text = 'Цель:'
                table.cell(1, 0).text = 'Процедура:'
                table.cell(2, 0).text = 'Ожидаемый результат:'

                table.cell(0, 1).text = test.purpose
                table.cell(1, 1).text = extraspace_filter(test.procedure)
                table.cell(2, 1).text = extraspace_filter(test.expected)

                # document.add_paragraph('test')
                # run.add_break()

        document.save('demo.docx')

        return HttpResponseRedirect('/testplan/' + testplan_id + '/')
    else:
        return HttpResponseRedirect('/testplan/')


def extraspace_filter(ctx):
    ctx = ctx.replace("\r\n** ", "\n** ")
    ctx = ctx.replace("\r\n* ", "\n* ")
    ctx = ctx.replace("\r\n# ", "\n# ")
    ctx = ctx.replace("\r", "")
    return ctx
