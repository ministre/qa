from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import DocxProfile
from .forms import DocxProfileForm
from django.shortcuts import get_object_or_404
from testplan.models import Testplan, Chapter, Category, Test, TestLink, TestChecklist, TestChecklistItem, TestConfig
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.shared import OxmlElement, qn
from django.utils.datastructures import MultiValueDictKeyError


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


def shade_cells(cells, shade):
    for cell in cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcVAlign = OxmlElement("w:shd")
        tcVAlign.set(qn("w:fill"), shade)
        tcPr.append(tcVAlign)


def build_testplan(request):
    if request.method == 'POST':
        testplan = get_object_or_404(Testplan, id=request.POST['testplan'])
        document = Document()
        # styles
        style = document.styles['Title']
        style.paragraph_format.space_before = Pt(5)
        style.font.size = Pt(20)
        style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        style = document.styles['Heading 1']
        style.paragraph_format.space_before = Pt(5)
        style.font.size = Pt(16)
        style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        style = document.styles['Heading 2']
        style.paragraph_format.space_before = Pt(5)
        style.font.size = Pt(14)
        style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        style = document.styles['Subtitle']
        style.paragraph_format.space_before = Pt(5)
        style.font.size = Pt(13)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        style = document.styles['Caption']
        style.paragraph_format.space_before = Pt(5)
        style.font.size = Pt(11)
        style.font.bold = True
        style.font.underline = True
        style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        # title
        document.add_paragraph(testplan.name, style='Title')

        # chapters
        try:
            if request.POST['chapters']:
                chapters = Chapter.objects.filter(testplan=testplan).order_by('id')
                if chapters:
                    for chapter in chapters:
                        document.add_heading(chapter.name, level=1)
                        paragraph = document.add_paragraph(chapter.text, style='Normal')
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        except MultiValueDictKeyError:
            pass

        # tests
        categories = Category.objects.filter(testplan=testplan).order_by('id')
        for i, category in enumerate(categories):
            document.add_heading(str(i+1) + '. ' + category.name, level=1)

            tests = Test.objects.filter(category=category).order_by('id')
            for j, test in enumerate(tests):
                document.add_heading(str(i+1) + '.' + str(j+1) + '. ' + test.name, level=2)

                # purpose
                try:
                    if request.POST['purpose']:
                        document.add_paragraph('Цель', style='Subtitle')
                        paragraph = document.add_paragraph(test.purpose, style='Normal')
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                except MultiValueDictKeyError:
                    pass

                # procedure
                try:
                    if request.POST['procedure']:
                        document.add_paragraph('Процедура', style='Subtitle')
                        paragraph = document.add_paragraph(test.procedure, style='Normal')
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                except MultiValueDictKeyError:
                    pass

                # expected
                try:
                    if request.POST['expected']:
                        document.add_paragraph('Ожидаемый результат', style='Subtitle')
                        paragraph = document.add_paragraph(test.expected, style='Normal')
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                except MultiValueDictKeyError:
                    pass

                # links
                try:
                    if request.POST['links']:
                        links = TestLink.objects.filter(test=test).order_by('id')
                        if links:
                            document.add_paragraph('Ссылки', style='Subtitle')
                            for link in links:
                                document.add_paragraph(link.name, style='Caption')
                                document.add_paragraph(link.url, style='List Bullet')
                except MultiValueDictKeyError:
                    pass

                # checklists
                try:
                    if request.POST['checklists']:
                        checklists = TestChecklist.objects.filter(test=test).order_by('id')
                        if checklists:
                            document.add_paragraph('Чек-листы', style='Subtitle')
                            for checklist in checklists:
                                document.add_paragraph(checklist.name, style='Caption')
                                checklist_items = TestChecklistItem.objects.filter(checklist=checklist).order_by('id')
                                for checklist_item in checklist_items:
                                    document.add_paragraph(checklist_item.name, style='List Bullet')
                except MultiValueDictKeyError:
                    pass

                # configs
                try:
                    if request.POST['configs']:
                        configs = TestConfig.objects.filter(test=test).order_by('id')
                        if configs:
                            document.add_paragraph('Конфигурация', style='Subtitle')
                            for config in configs:
                                document.add_paragraph(config.name, style='Caption')
                                config.config = config.config.replace('\r', '')
                                table = document.add_table(rows=1, cols=1)
                                table.style = 'Table Grid'
                                shade_cells([table.cell(0, 0)], "#e3e8ec")
                                table.cell(0, 0).text = config.config
                except MultiValueDictKeyError:
                    pass

        testplan_filename = settings.MEDIA_ROOT + '/testplan_' + str(testplan.id) + '.docx'
        document.save(testplan_filename)

        file_path = os.path.join(settings.MEDIA_ROOT, testplan_filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
