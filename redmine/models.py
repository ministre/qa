from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError
from requests.exceptions import ConnectionError
from device.models import DeviceType, Device, Specification, Sample
from testplan.models import Pattern, Testplan, Category, Test, TestConfig, TestLink


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
        if self.get_project()[0]:
            try:
                self.redmine.wiki_page.get(wiki_title, project_id=self.project_id)
                if wiki_title == 'wiki':
                    return [True, settings.REDMINE_URL + '/projects/' + self.project_id + '/wiki/']
                else:
                    return [True, settings.REDMINE_URL + '/projects/' + self.project_id + '/wiki/' + wiki_title]
            except ResourceNotFoundError:
                return [False, 'Wiki not found']
            except ForbiddenError:
                return [False, 'Requested wiki resource is forbidden']
        else:
            return [False, self.get_project()[1]]

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
        specs = Specification().get_values(device)
        s = ''
        for spec in specs:
            s += '\nh3. ' + spec['name'] + '\n\n'
            for value in spec['values']:
                s += '* ' + value.name + '\n'

        samples = Sample.objects.filter(device=device)
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
        configs = TestConfig.objects.filter(test=test)
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

        links = TestLink.objects.filter(test=test)
        if links.count():
            wiki_links = '\nh2. Ссылки\n'
            for link in links:
                wiki_links += '\n> ' + link.name + '\n' + \
                              '\n' + link.url + '\n'
        else:
            wiki_links = ''

        wiki_text = 'h1. ' + test.name + '\n' + \
                    '\nh2. Цель\n\n' + test.purpose + '\n' + \
                    '\nh2. Процедура\n\n' + test.procedure + '\n' + \
                    wiki_configs + \
                    '\nh2. Ожидаемый результат\n\n' + test.expected + '\n' + \
                    wiki_links
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
