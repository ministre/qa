from django.shortcuts import render
from django.shortcuts import get_object_or_404
from testplan.models import Testplan
from docx import Document


# Create your views here.
def build_testplan(request):
    if request.method == 'POST':
        testplan = get_object_or_404(Testplan, id=request.POST['testplan'])
        document = Document()
