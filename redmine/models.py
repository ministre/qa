from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError
from requests.exceptions import ConnectionError
from device.models import DeviceType, Device, Specification, Sample
from testplan.models import Pattern, Testplan, Category, Test, TestConfig, TestLink, TestChecklist, TestChecklistItem, \
    TestComment, TestImage
import re


class RedmineTest(object):
    def __init__(self, wiki_title: str):
        self.wiki_title = wiki_title
        self.wiki = ''
        self.wiki_name = ''
        self.wiki_purpose = ''
        self.wiki_procedure = ''
        self.wiki_configs = ''
        self.wiki_expected = ''
        self.wiki_checklists = ''
        self.wiki_links = ''
        self.wiki_comments = ''

    def set_wiki(self, wiki_text: str):
        self.wiki = wiki_text
        return self.wiki

    def collect_wiki(self):
        self.wiki = self.wiki_name + self.wiki_purpose + self.wiki_procedure + self.wiki_configs + \
                    self.wiki_expected + self.wiki_checklists + self.wiki_links + self.wiki_comments
        return self.wiki

    def parse_name(self):
        blocks = self.wiki.split('\r')
        name = blocks[0][4:]
        return name

    def set_name(self, text: str):
        self.wiki_name = 'h1. ' + text + '\r\n\r'
        return self.collect_wiki()

    def parse_purpose(self):
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Цель\r', h2_block)
            if detect_head:
                purpose = h2_block.split('\r\n')[2]
                return purpose
        return False

    def set_purpose(self, text: str):
        self.wiki_purpose = '\nh2. Цель\r\n\r\n' + text + '\r\n\r'
        return self.collect_wiki()

    def parse_procedure(self):
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Процедура\r', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                procedure_blocks = h3_blocks[0].split('\n')
                procedure = procedure_blocks[2][:-1]
                return procedure
        return False

    def set_procedure(self, text: str):
        self.wiki_procedure = '\nh2. Процедура\r\n\r\n' + text + '\r\n\r'
        return self.collect_wiki()

    def parse_configs(self):
        configs = []
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Конфигурация\r', h2_block)
            if detect_head:
                configs_blocks = h2_block.split('\n{{collapse(')
                configs_blocks.pop(0)
                for configs_block in configs_blocks:
                    config_blocks = configs_block.split(')\r\n<pre><code class="')
                    config = []
                    name = config_blocks[0]
                    lang = config_blocks[1].split('"')[0]
                    code = config_blocks[1].split('\r\n</code></pre>\r\n}}')[0][config_blocks[1].find('">\r\n')+4:]
                    config.append(name)
                    config.append(lang)
                    config.append(code)
                    configs.append(config)
        return configs

    def set_configs(self, configs):
        self.wiki_configs = '\nh2. Конфигурация\r\n'
        for config in configs:
            if config.lang == 'json':
                config.lang = 'javascript'
            self.wiki_configs += '\n{{collapse(' + config.name + ')\r' + \
                                 '\n<pre><code class="' + config.lang + '">\r' + \
                                 '\n' + config.config + '\r' + \
                                 '\n</code></pre>\r' + \
                                 '\n}}\r\n\r'
        return self.collect_wiki()

    def parse_images(self):
        return False

    def parse_files(self):
        return False

    def parse_expected(self):
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Ожидаемый результат\r', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                expected = h3_blocks[0][h3_blocks[0].find('\r\n\r\n')+4:-3]
                return expected
        return False

    def set_expected(self, text: str):
        self.wiki_expected = '\nh2. Ожидаемый результат\r\n\r\n' + text + '\r\n\r'
        return self.collect_wiki()

    def parse_checklists(self):
        checklists = []
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Ожидаемый результат\r', h2_block)
            if detect_head:
                for h3_block in h2_block.split('\nh3. '):
                    detect_checklist_head = re.search('Чек-листы\r', h3_block)
                    if detect_checklist_head:
                        h4_blocks = h3_block.split('\nh4. ')
                        h4_blocks.pop(0)
                        for h4_block in h4_blocks:
                            checklist_blocks = h4_block.split('\r\n* ')
                            name = checklist_blocks[0][:-2]
                            checklist_blocks.pop(0)
                            items = []
                            for item in checklist_blocks:
                                item = item.replace("\n", "")
                                item = item.replace("\r", "")
                                items.append(item)
                            checklist = {'name': name, 'items': items}
                            checklists.append(checklist)
        return checklists

    def set_checklists(self, checklists):
        if checklists:
            self.wiki_checklists += '\nh3. Чек-листы' + '\r\n\r'
        for checklist in checklists:
            self.wiki_checklists += '\nh4. ' + checklist.name + '\r'
            checklist_items = TestChecklistItem.objects.filter(checklist=checklist)
            self.wiki_checklists += '\n\r'
            for checklist_item in checklist_items:
                self.wiki_checklists += '\n* ' + checklist_item.name + '\r'
            self.wiki_checklists += '\n\r'
        return self.collect_wiki()

    def parse_links(self):
        links = []
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Ссылки\r', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                h3_blocks.pop(0)
                for h3_block in h3_blocks:
                    link = []
                    link_blocks = h3_block.split('\r\n\r\n')
                    name = link_blocks[0]
                    url = link_blocks[1]
                    url = url.replace('\n', '')
                    url = url.replace('\r', '')
                    link.append(name)
                    link.append(url)
                    links.append(link)
        return links

    def set_links(self, links):
        if links:
            self.wiki_checklists += '\nh2. Ссылки' + '\r\n\r'
            for link in links:
                self.wiki_checklists += '\nh3. ' + link.name + '\r\n\r'
                self.wiki_checklists += '\n' + link.url + '\r\n\r'
        return self.collect_wiki()

    def parse_comments(self):
        comments = []
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Комментарии\r', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                h3_blocks.pop(0)
                for h3_block in h3_blocks:
                    comment = []
                    comment_blocks = h3_block.split('\r\n\r\n')
                    name = comment_blocks[0]
                    text = comment_blocks[1]
                    text = text.replace('\r\n\r', '')
                    comment.append(name)
                    comment.append(text)
                    comments.append(comment)
        return comments

    def set_comments(self, comments):
        if comments:
            self.wiki_comments += '\nh2. Комментарии' + '\r\n\r'
            for comment in comments:
                self.wiki_comments += '\nh3. ' + comment.name + '\r\n\r'
                self.wiki_comments += '\n' + comment.text + '\r\n\r'
        return self.collect_wiki()


class RedmineProject(object):
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.0.4')

    def check_project(self):
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

    def check_wiki(self, title: str):
        try:
            wiki_text = self.redmine.wiki_page.get(title, project_id=self.project_id)
            return [True, wiki_text.text]
        except ResourceNotFoundError:
            return[False, 'Wiki not found']
        except ForbiddenError:
            return [False, 'Requested wiki resource is forbidden']

    def create_test(self, r_test: RedmineTest):
        self.redmine.wiki_page.create(project_id=self.project_id, title=r_test.wiki_title, text=r_test.wiki,
                                      parent_title='wiki')
        return True

    def update_test(self, r_test: RedmineTest):
        self.redmine.wiki_page.update(r_test.wiki_title, project_id=self.project_id, text=r_test.wiki)
        return True


    def export_device_type(self, device_type: DeviceType):
        if self.check_project()[0]:
            self.redmine.project.update(self.check_project()[1], name=device_type.redmine_project_name)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text='h1. ' + device_type.desc)
            return [True, 'Project updated successfully']
        elif self.check_project()[1] == 'Project not found':
            self.redmine.project.create(name=device_type.redmine_project_name, identifier=self.project_id,
                                        inherit_members=True)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text='h1. ' + device_type.desc)
            return [True, 'Project created']
        else:
            return [False, self.check_project()[1]]

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

        if self.check_project()[0]:
            self.redmine.project.update(self.check_project()[1], name=device.vendor.name + ' ' + device.model)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text=wiki_text)
            return [True, 'Project updated successfully']
        elif self.check_project()[1] == 'Project not found':
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
            wiki_configs = '\nh3. Конфигурация\r'
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
            wiki_links = '\nh2. Ссылки\r'
            for link in links:
                wiki_links += '\nh3. ' + link.name + '\r' + \
                              '\n' + link.url + '\r'
        else:
            wiki_links = ''

        checklists = TestChecklist.objects.filter(test=test).order_by('id')
        wiki_checklists = ''
        for checklist in checklists:
            wiki_checklists += '\nh3. Чек-лист\r\n\r'
            wiki_checklists += '\n' + checklist.name + '\r\n\r'
            checklist_items = TestChecklistItem.objects.filter(checklist=checklist)
            for checklist_item in checklist_items:
                wiki_checklists += '\n* ' + checklist_item.name + '\r'
            wiki_checklists += '\n\r'

        comments = TestComment.objects.filter(test=test).order_by('id')
        if comments.count():
            wiki_comments = '\nh2. Комментарии\r' + '\n\r'
            for comment in comments:
                wiki_comments += '\nh3. ' + comment.name + '\r\n\r' + \
                                 '\n' + comment.text + '\r\n\r'
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
                    wiki_checklists + \
                    wiki_links +\
                    wiki_comments

        if self.check_project()[0]:
            if self.check_wiki(test.redmine_wiki)[0]:
                self.redmine.wiki_page.update(test.redmine_wiki, project_id=test.category.testplan.redmine_project,
                                              text=wiki_text)
                return [True, 'Wiki updated successfully']
            else:
                self.redmine.wiki_page.create(project_id=test.category.testplan.redmine_project,
                                              title=test.redmine_wiki, text=wiki_text, parent_title='wiki')
                return [True, 'Wiki created successfully']

        elif self.check_project()[1] == 'Project not found':
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
        if self.check_project()[0]:
            self.redmine.project.update(self.check_project()[1], name=pattern.name)
            self.redmine.wiki_page.update('Wiki', project_id=self.project_id, text=wiki_text)
            return [True, 'Project updated successfully']

        elif self.check_project()[1] == 'Project not found':
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

        if self.check_project()[0]:
            self.redmine.project.update(self.check_project()[1], name=testplan.name)
            self.redmine.wiki_page.update('wiki', project_id=self.project_id, text=wiki_text)
            self.export_all_tests(testplan)
            return [True, 'Project updated successfully']

        elif self.check_project()[1] == 'Project not found':
            parent_id = self.redmine.project.get(testplan.redmine_parent).id
            self.redmine.project.create(name=testplan.name,
                                        identifier=self.project_id,
                                        parent_id=parent_id,
                                        inherit_members=True)
            self.redmine.wiki_page.update('wiki', project_id=self.project_id, text=wiki_text)
            self.export_all_tests(testplan)
            return [True, 'Project created']

