from testplan.models import Testplan
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from docx import Document


@login_required
def build_testplan(request):
    if request.method == 'POST':
        testplan = get_object_or_404(Testplan, id=request.POST['testplan_id'])
        document = Document()
        document.add_paragraph('test')
        document.save('demo.docx')
