from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import DocxProfile
from .forms import DocxProfileForm
from django.shortcuts import get_object_or_404
from testplan.models import Testplan, Category, Test
from docx import Document
from docx.shared import Pt, RGBColor
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class DocxProfileCreate(CreateView):
    model = DocxProfile
    form_class = DocxProfileForm
    template_name = 'docx_builder/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_profiles')
        return context

    def get_success_url(self):
        return reverse('docx_profiles')


@method_decorator(login_required, name='dispatch')
class DocxProfileUpdate(UpdateView):
    model = DocxProfile
    form_class = DocxProfileForm
    template_name = 'docx_builder/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': datetime.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_profiles')
        return context

    def get_success_url(self):
        self.object.update_timestamp(user=self.request.user)
        return reverse('docx_profiles')


@method_decorator(login_required, name='dispatch')
class DocxProfileDelete(DeleteView):
    model = DocxProfile
    template_name = 'docx_builder/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_profiles')
        return context

    def get_success_url(self):
        return reverse('docx_profiles')


@method_decorator(login_required, name='dispatch')
class DocxProfileListView(ListView):
    context_object_name = 'docx_profiles'
    queryset = DocxProfile.objects.all()
    template_name = 'docx_builder/list.html'


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
