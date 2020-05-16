from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError
from requests.exceptions import ConnectionError
from device.models import DeviceType, Device, Specification, Sample
from testplan.models import Pattern, Testplan, Category, Test, TestConfig, TestLink, TestWorksheet, TestWorksheetItem, \
    TestComment, TestImage
import re


class RedmineProject(object):
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.0.4')

    def get_project(self):
        try:
            project = self.redmine.project.get(self.project_id)
            return [True, project.id]
        except ConnectionError:
            return [False, 'Connection error']
        except AuthError:
            return [False, 'Authentication error']
        except ResourceNotFoundError:
            return [False, 'Project not found']
        except ForbiddenError:
            return [False, 'Requested project resource is forbidden']

    def get_wiki_url(self, wiki_title: str):
        try:
            self.redmine.wiki_page.get(wiki_title, project_id=self.project_id)
            if wiki_title == 'wiki':
                return [True, settings.REDMINE_URL + '/projects/' + self.project_id + '/wiki/']
            else:
                return [True, settings.REDMINE_URL + '/projects/' + self.project_id + '/wiki/' + wiki_title]
        except ResourceNotFoundError:
            return[False, 'Wiki not found']
        except ForbiddenError:
            return [False, 'Requested wiki resource is forbidden']

    def get_wiki_text(self, wiki_title: str):
        try:
            wiki = self.redmine.wiki_page.get(wiki_title, project_id=self.project_id)
            return [True, wiki.text]
        except ResourceNotFoundError:
            return[False, 'Wiki not found']
        except ForbiddenError:
            return [False, 'Requested wiki resource is forbidden']

    def export_device_type(self, device_type: DeviceType):
        if self.get_project()[0]:
            self.redmine.project.update(self.get_project()[1], name=device_type.redmine_project_name)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text='h1. ' + device_type.desc)
            return [True, 'Project updated successfully']
        elif self.get_project()[1] == 'Project not found':
            self.redmine.project.create(name=device_type.redmine_project_name, identifier=self.project_id,
                                        inherit_members=True)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text='h1. ' + device_type.desc)
            return [True, 'Project created']
        else:
            return [False, self.get_project()[1]]

    def export_device(self, device: Device):
        specs = Specification().get_values(device).order_by('id')
        s = ''
        for spec in specs:
            s += '\nh3. ' + spec['name'] + '\n\n'
            for value in spec['values']:
                s += '* ' + value.name + '\n'

        samples = Sample.objects.filter(device=device).order_by('id')
        sm = ''
        for sample in samples:
            sm += '\nh3. ' + sample.sn + '\n\n' + \
                '| User login: | ' + sample.user_login + '|\n' + \
                '| User password: | ' + sample.user_password + '|\n' + \
                '| Support login: | ' + sample.support_login + '|\n' + \
                '| Support password: | ' + sample.support_password + '|\n'

        wiki_text = '__%{color:white}' + device.type.redmine_project + \
                    '%__\n\n---\n\nh1. ' + device.vendor.name + ' ' + device.model + '\n' +\
                    '\nh2. Внешний вид\n' + \
                    '\nh2. Общая информация\n' + \
                    '\n| Производитель: | ' + device.vendor.name + ' |\n| Модель: | ' + \
                    device.model + ' |\n| Версия Hardware: | ' + device.hw + ' |\n' + \
                    '\nh2. Технические характеристики\n' + \
                    '\n' + s + '\n' + \
                    '\nh2. Тестовые образцы\n' + \
                    '\n' + sm + '\n' + \
                    '\nh2. Результаты испытаний\n'

        if self.get_project()[0]:
            self.redmine.project.update(self.get_project()[1], name=device.vendor.name + ' ' + device.model)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text=wiki_text)
            return [True, 'Project updated successfully']
        elif self.get_project()[1] == 'Project not found':
            parent_id = self.redmine.project.get(device.type.redmine_project).id
            self.redmine.project.create(name=device.vendor.name + ' ' + device.model,
                                        identifier=self.project_id,
                                        parent_id=parent_id,
                                        inherit_members=True)

            self.redmine.wiki_page.update('wiki', project_id=self.project_id, text=wiki_text)
            return [True, 'Project created']

    def export_test(self, test: Test):
        configs = TestConfig.objects.filter(test=test).order_by('id')
        if configs.count():
            wiki_configs = '\nh3. Конфигурация\n'
            for config in configs:
                if config.lang == 'json':
                    lang = 'javascript'
                else:
                    lang = config.lang
                wiki_configs += '\n{{collapse(' + config.name + ')\n' + \
                                '\n<pre><code class="' + lang + '">\n' + \
                                '\n' + config.config + '\n' + \
                                '</code></pre>\n' + \
                                '}}\n'
        else:
            wiki_configs = ''

        links = TestLink.objects.filter(test=test).order_by('id')
        if links.count():
            wiki_links = '\nh2. Ссылки\n'
            for link in links:
                wiki_links += '\nh3. ' + link.name + '\n' + \
                              '\n' + link.url + '\n'
        else:
            wiki_links = ''

        worksheets = TestWorksheet.objects.filter(test=test).order_by('id')
        wiki_worksheets = ''
        for worksheet in worksheets:
            if worksheet.type == 'text':
                wiki_worksheets += '\nh3. Текстовое значение\n'
            elif worksheet.type == 'number':
                wiki_worksheets += '\nh3. Численное значение\n'
            elif worksheet.type == 'checklist':
                wiki_worksheets += '\nh3. Чек-лист\n'
            elif worksheet.type == 'table':
                wiki_worksheets += '\nh3. Таблица\n'
            wiki_worksheets += '\n' + worksheet.name + '\n'
            if worksheet.type == 'checklist' or worksheet.type == 'table':
                worksheet_items = TestWorksheetItem.objects.filter(worksheet=worksheet)
                for worksheet_item in worksheet_items:
                    wiki_worksheets += '\n* ' + worksheet_item.name
                wiki_worksheets += '\n'

        comments = TestComment.objects.filter(test=test).order_by('id')
        if comments.count():
            wiki_comments = '\nh2. Комментарии\n'
            for comment in comments:
                wiki_comments += '\nh3. ' + comment.name + '\n' + \
                                 '\n' + comment.text + '\n'
        else:
            wiki_comments = ''

        images = TestImage.objects.filter(test=test)
        if images.count():
            wiki_images = '\nh3. Изображения\n'
            for image in images:
                wiki_images += '\n> ' + image.name + '\n' + \
                    '\n' + image.image.url + '\n'
        else:
            wiki_images = ''

        wiki_text = 'h1. ' + test.name + '\n' + \
                    '\nh2. Цель\n\n' + test.purpose + '\n' + \
                    '\nh2. Процедура\n\n' + test.procedure + '\n' + \
                    wiki_images + \
                    wiki_configs + \
                    '\nh2. Ожидаемый результат\n\n' + test.expected + '\n' + \
                    wiki_worksheets + \
                    wiki_links +\
                    wiki_comments

        if self.get_project()[0]:
            if self.get_wiki_url(test.redmine_wiki)[0]:
                self.redmine.wiki_page.update(test.redmine_wiki, project_id=test.category.testplan.redmine_project,
                                              text=wiki_text)
                return [True, 'Wiki updated successfully']
            else:
                self.redmine.wiki_page.create(project_id=test.category.testplan.redmine_project,
                                              title=test.redmine_wiki, text=wiki_text, parent_title='wiki')
                return [True, 'Wiki created successfully']

        elif self.get_project()[1] == 'Project not found':
            return [False, 'Project not found']

    def export_all_tests(self, testplan: Testplan):
        categories = Category.objects.filter(testplan=testplan).order_by('id')
        for category in categories:
            tests = Test.objects.filter(category=category).order_by('id')
            for test in tests:
                self.export_test(test)
        return True

    def export_pattern(self, pattern: Pattern):
        wiki_text = 'h1. ' + pattern.name
        if self.get_project()[0]:
            self.redmine.project.update(self.get_project()[1], name=pattern.name)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text=wiki_text)
            return [True, 'Project updated successfully']

        elif self.get_project()[1] == 'Project not found':
            parent_id = self.redmine.project.get(pattern.redmine_parent).id
            self.redmine.project.create(name=pattern.name,
                                        identifier=self.project_id,
                                        parent_id=parent_id,
                                        inherit_members=True)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text=wiki_text)
        return [True, 'Project created']

    def export_testplan(self, testplan: Testplan):
        categories = Category.objects.filter(testplan=testplan).order_by('id')
        wiki_testlist = ''
        for category in categories:
            wiki_testlist += '\nh2. ' + category.name + '\n'
            tests = Test.objects.filter(category=category).order_by('id')
            for test in tests:
                wiki_testlist += '\n* [[' + test.redmine_wiki + '|' + test.name + ']]'
            wiki_testlist += '\n'
        wiki_text = 'h1. ' + testplan.name + '\n' + wiki_testlist

        if self.get_project()[0]:
            self.redmine.project.update(self.get_project()[1], name=testplan.name)
            self.redmine.wiki_page.update('wiki', project_id=self.project_id, text=wiki_text)
            self.export_all_tests(testplan)
            return [True, 'Project updated successfully']

        elif self.get_project()[1] == 'Project not found':
            parent_id = self.redmine.project.get(testplan.redmine_parent).id
            self.redmine.project.create(name=testplan.name,
                                        identifier=self.project_id,
                                        parent_id=parent_id,
                                        inherit_members=True)
            self.redmine.wiki_page.update('wiki', project_id=self.project_id, text=wiki_text)
            self.export_all_tests(testplan)
            return [True, 'Project created']


class RedmineTest(object):
    def __init__(self, wiki: str):
        self.wiki = wiki
        self.h2_blocks = wiki.split('\nh2. ')

    def parse_name(self):
        for h2_block in self.h2_blocks:
            detect_head = re.search('h1. ', h2_block)
            if detect_head:
                name_blocks = h2_block.split('\r')
                name = name_blocks[0][4:]
                return name
        return False

    def parse_purpose(self):
        for h2_block in self.h2_blocks:
            detect_head = re.search('Цель\n', h2_block)
            if detect_head:
                purpose_blocks = h2_block.split('\n\n')
                purpose_blocks.pop(0)
                purpose = '\n\n'.join(purpose_blocks)[0:-1]
                return purpose
        return False

    def parse_procedure(self):
        for h2_block in self.h2_blocks:
            detect_head = re.search('Процедура\n', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                procedure_blocks = h3_blocks[0].split('\n\n')
                procedure_blocks.pop(0)
                procedure = '\n\n'.join(procedure_blocks)[0:-1]
                return procedure
        return False

    def parse_expected(self):
        for h2_block in self.h2_blocks:
            detect_head = re.search('Ожидаемый результат\n', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                expected_blocks = h3_blocks[0].split('\n\n')
                expected_blocks.pop(0)
                expected = '\n\n'.join(expected_blocks)[0:-1]
                return expected
        return False

    def parse_configs(self):
        configs = []
        procedure = self.h2_blocks[2].split('\nh3. ')
        for i, procedure_block in enumerate(procedure):
            detect_head = re.search('Конфигурация\n', procedure_block)
            if detect_head:
                cfg = procedure[i].split('\n{{collapse(')
                for j, cfg_block in enumerate(cfg):
                    detect_code = re.search('<pre><code class=', cfg_block)
                    if detect_code:
                        config = []  # name, lang, configuration
                        code_name = cfg[j].split(')\n')[0]
                        code_lang = cfg[j].split('"')[1]
                        s_cfg = cfg[j].split('">\n\n')[1]
                        code_cfg = s_cfg.split('\n</code></pre>\n')[0]
                        config.append(code_name)
                        config.append(code_lang)
                        config.append(code_cfg)
                        configs.append(config)
        return configs

    def parse_images(self):
        return False

    def parse_files(self):
        return False

    def parse_worksheets(self):
        return False

    def parse_links(self):
        links = []
        for h2_block in self.h2_blocks:
            detect_head = re.search('Ссылки\n', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                h3_blocks.pop(0)
                for h3_block in h3_blocks:
                    link = []
                    link_blocks = h3_block.split('\n\n')
                    link_name = link_blocks[0]
                    link_url = link_blocks[1][0:-1]
                    link.append(link_name)
                    link.append(link_url)
                    links.append(link)
                return links
        return False

    def parse_comments(self):
        comments = []
        for h2_block in self.h2_blocks:
            detect_head = re.search('Комментарии\n\n', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('h3. ')
                h3_blocks.remove('Комментарии\n\n')
                for h3_block in h3_blocks:
                    comment = []  # name, text
                    comment_blocks = h3_block.split('\n\n')
                    comment_name = comment_blocks[0]
                    comment_blocks.pop(0)
                    comment_text = '\n\n'.join(comment_blocks)
                    comment.append(comment_name)
                    comment.append(comment_text)
                    comments.append(comment)
        return comments
