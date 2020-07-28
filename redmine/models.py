from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError, ValidationError
from requests.exceptions import ConnectionError
from testplan.models import TestChecklistItem, Chapter, Test, TestConfig, TestImage, TestFile, TestChecklist, TestLink,\
    TestComment
from feature.models import FeatureList, FeatureListCategory, FeatureListItem
import re
from device.models import DeviceType, DeviceTypeSpecification


class RedmineProject(object):
    def __init__(self):
        self.redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.0.4')

    def check_project(self, project: str):
        try:
            p = self.redmine.project.get(project)
            return [True, p.id]
        except ConnectionError:
            return [False, 'Connection error']
        except AuthError:
            return [False, 'Authentication error']
        except ResourceNotFoundError:
            return [False, 'Project not found']
        except ForbiddenError:
            return [False, 'Requested project resource is forbidden']

    def check_wiki(self, project: str, wiki_title: str):
        try:
            wiki_text = self.redmine.wiki_page.get(wiki_title, project_id=project)
            return [True, wiki_text.text]
        except ResourceNotFoundError:
            return[False, 'Wiki not found']
        except ForbiddenError:
            return [False, 'Requested wiki resource is forbidden']

    def create_or_update_project(self, project: str, project_name: str, parent='', description=None):
        is_project = self.check_project(project=project)
        if is_project[0]:
            # update project
            if description:
                self.redmine.project.update(resource_id=is_project[1], name=project_name,
                                            description='__%{color:gray}' + description + '%__')
            else:
                self.redmine.project.update(resource_id=is_project[1], name=project_name)
            return [True, 'Project updated']
        else:
            if is_project[1] == 'Project not found':
                if parent:
                    is_parent_project = self.check_project(project=parent)
                    if is_parent_project[0]:
                        # create sub-project
                        try:
                            if description:
                                p = self.redmine.project.create(identifier=project, name=project_name,
                                                                parent_id=is_parent_project[1], inherit_members=True,
                                                                description='__%{color:gray}' + description + '%__')
                            else:
                                p = self.redmine.project.create(identifier=project, name=project_name,
                                                                parent_id=is_parent_project[1], inherit_members=True)
                            return [True, p.id]
                        except ValidationError:
                            return [False, 'Sub-project name validation fail']
                    else:
                        if is_parent_project[1] == 'Project not found':
                            return [False, 'Parent project not found']
                        else:
                            return [False, 'Parent project - ' + is_parent_project[1]]
                else:
                    # create root project
                    try:
                        if description:
                            p = self.redmine.project.create(identifier=project, name=project_name, inherit_members=True,
                                                            description='__%{color:gray}' + description + '%__')
                        else:
                            p = self.redmine.project.create(identifier=project, name=project_name, inherit_members=True)
                        return [True, p.id]
                    except ValidationError:
                        return [False, 'Root project name validation error']
            else:
                return [False, is_project[1]]

    def create_or_update_wiki(self, project: str, wiki_title: str, wiki_text: str, parent_title=None):
        is_wiki = self.check_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0]:
            if parent_title:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text, parent_title='wiki')
            else:
                self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text)
            return [True, 'Wiki has been updated']
        else:
            if is_wiki[1] == 'Wiki not found':
                if parent_title:
                    self.redmine.wiki_page.create(project_id=project, title=wiki_title, text=wiki_text,
                                                  parent_title='wiki')
                else:
                    self.redmine.wiki_page.create(project_id=project, title=wiki_title, text=wiki_text)
                return [True, 'Wiki has been created']
            else:
                return [False, is_wiki[1]]


class RedmineChapter(object):
    def __init__(self):
        self.wiki = ''
        self.ctx = ''

    def get_wiki_chapter(self, chapter: Chapter):
        self.ctx = 'h1. ' + chapter.name + '\r\n\r\n' + chapter.text + '\r'
        return self.ctx

    def export(self, project: str, wiki_title: str, chapter: Chapter):
        self.wiki += self.get_wiki_chapter(chapter)
        is_wiki = RedmineProject().create_or_update_wiki(project=project, wiki_title=wiki_title, wiki_text=self.wiki,
                                                         parent_title='wiki')
        return is_wiki

    def parse_details(self, project: str, wiki_title: str):
        is_wiki = RedmineProject().check_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0]:
            self.wiki = is_wiki[1]
            chapter_blocks = self.wiki.split('\r\n')
            name = chapter_blocks.pop(0)[4:]
            text = '\r\n'.join(chapter_blocks)[2:-1]
            return [True, {'name': name, 'text': text}]
        else:
            return [False, is_wiki[1]]


class RedmineTest(object):
    def __init__(self):
        self.wiki = ''

    def parse_name(self):
        blocks = self.wiki.split('\r')
        name = blocks[0][4:]
        return name

    def get_wiki_name(self, text: str):
        ctx = 'h1. ' + text + '\r\n\r'
        return ctx

    def parse_purpose(self):
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Цель\r', h2_block)
            if detect_head:
                purpose = h2_block.split('\r\n')[2]
                return purpose
        return False

    def get_wiki_purpose(self, text: str):
        ctx = '\nh2. Цель\r\n\r\n' + text + '\r\n\r'
        return ctx

    def parse_procedure(self):
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Процедура\r', h2_block)
            if detect_head:
                procedure = h2_block.split('\nh3. ')[0][13:]
                return procedure
        return False

    def get_wiki_procedure(self, text: str):
        ctx = '\nh2. Процедура\r\n\r\n' + text + '\r\n\r'
        return ctx

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

    def get_wiki_configs(self, configs):
        ctx = ''
        if configs:
            ctx = '\nh2. Конфигурация\r\n'
            for config in configs:
                if config.lang == 'json':
                    config.lang = 'javascript'
                ctx += '\n{{collapse(' + config.name + ')\r' + \
                       '\n<pre><code class="' + config.lang + '">\r' + \
                       '\n' + config.config + '\r' + \
                       '\n</code></pre>\r' + \
                       '\n}}\r\n\r'
        return ctx

    def parse_images(self):
        return []

    def parse_files(self):
        return []

    def parse_expected(self):
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Ожидаемый результат\r', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                expected = h3_blocks[0][h3_blocks[0].find('\r\n\r\n')+4:-3]
                return expected
        return False

    def get_wiki_expected(self, text: str):
        ctx = '\nh2. Ожидаемый результат\r\n\r\n' + text + '\r\n\r'
        return ctx

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

    def get_wiki_checklists(self, checklists):
        ctx = ''
        if checklists:
            ctx += '\nh3. Чек-листы' + '\r\n\r'
            for checklist in checklists:
                ctx += '\nh4. ' + checklist.name + '\r'
                checklist_items = TestChecklistItem.objects.filter(checklist=checklist).order_by('id')
                ctx += '\n\r'
                for checklist_item in checklist_items:
                    ctx += '\n* ' + checklist_item.name + '\r'
                ctx += '\n\r'
        return ctx

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

    def get_wiki_links(self, links):
        ctx = ''
        if links:
            ctx += '\nh2. Ссылки' + '\r\n\r'
            for link in links:
                ctx += '\nh3. ' + link.name + '\r\n\r'
                ctx += '\n' + link.url + '\r\n\r'
        return ctx

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

    def get_wiki_comments(self, comments):
        ctx = ''
        if comments:
            ctx += '\nh2. Комментарии' + '\r\n\r'
            for comment in comments:
                ctx += '\nh3. ' + comment.name + '\r\n\r'
                ctx += '\n' + comment.text + '\r\n\r'
        return ctx

    def parse_details(self, project: str, wiki_title: str, is_purpose: bool, is_procedure: bool,
                      is_configs: bool, is_images: bool, is_files: bool, is_expected: bool, is_checklists: bool,
                      is_links: bool, is_comments: bool):
        is_wiki = RedmineProject().check_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0]:
            self.wiki = is_wiki[1]
            name = self.parse_name()
            if is_purpose:
                purpose = self.parse_purpose()
            else:
                purpose = None
            if is_procedure:
                procedure = self.parse_procedure()
            else:
                procedure = None
            if is_configs:
                configs = self.parse_configs()
            else:
                configs = None
            if is_images:
                images = self.parse_images()
            else:
                images = None
            if is_files:
                files = self.parse_files()
            else:
                files = None
            if is_expected:
                expected = self.parse_expected()
            else:
                expected = None
            if is_checklists:
                checklists = self.parse_checklists()
            else:
                checklists = None
            if is_links:
                links = self.parse_links()
            else:
                links = None
            if is_comments:
                comments = self.parse_comments()
            else:
                comments = None
            return [True, {'name': name, 'purpose': purpose, 'procedure': procedure, 'configs': configs,
                           'images': images, 'files': files, 'expected': expected, 'checklists': checklists,
                           'links': links, 'comments': comments}]
        else:
            return [False, is_wiki[1]]

    def export(self, project: str, wiki_title: str, name: str, purpose, procedure, configs, images, files,
               expected, checklists, links, comments):
        self.wiki += self.get_wiki_name(name)
        if purpose:
            self.wiki += self.get_wiki_purpose(text=purpose)
        if procedure:
            self.wiki += self.get_wiki_procedure(text=procedure)
        if configs:
            self.wiki += self.get_wiki_configs(configs=configs)
        if expected:
            self.wiki += self.get_wiki_expected(text=expected)
        if checklists:
            self.wiki += self.get_wiki_checklists(checklists=checklists)
        if links:
            self.wiki += self.get_wiki_links(links=links)
        if comments:
            self.wiki += self.get_wiki_comments(comments=comments)

        wiki_page = RedmineProject().create_or_update_wiki(project=project, wiki_title=wiki_title, wiki_text=self.wiki,
                                                           parent_title='wiki')
        return wiki_page


class RedmineTestplan(object):
    def __init__(self):
        self.wiki = ''

    def get_wiki_chapters(self, chapters):
        ctx = '\nh2. Общие положения\r\n\r'
        for chapter in chapters:
            if chapter.redmine_wiki:
                ctx += '\n* [[' + chapter.redmine_wiki + '|' + chapter.name + ']]\r'
            else:
                ctx += '\n* ' + chapter.name + '\r'
        ctx += '\n\r'
        return ctx

    def get_wiki_categories(self, categories):
        ctx = '\nh2. Список тестов\r\n\r'
        for category in categories:
            ctx += '\nh3. ' + category.name + '\r\n\r'
            tests = Test.objects.filter(category=category).order_by('id')
            for test in tests:
                if test.redmine_wiki:
                    ctx += '\n* [[' + test.redmine_wiki + '|' + test.name + ']]\r'
                else:
                    ctx += '\n* ' + test.name + '\r'
            ctx += '\n\r'
        return ctx

    def export(self, project: str, project_name: str, parent: str, version: str, chapters, categories):
        r = RedmineProject()
        redmine_project = r.create_or_update_project(project=project, project_name=project_name, parent=parent,
                                                     description=version)
        if redmine_project[0]:
            # build testplan wiki
            self.wiki = 'h1. ' + project_name + '\r\n\r'
            if chapters:
                self.wiki += self.get_wiki_chapters(chapters)
            if categories:
                self.wiki += self.get_wiki_categories(categories)
            is_wiki = r.create_or_update_wiki(project=project, wiki_title='Wiki', wiki_text=self.wiki)

            # build items wiki
            if chapters:
                for chapter in chapters:
                    if chapter.redmine_wiki:
                        redmine_chapter = RedmineChapter()
                        redmine_chapter.export(project=project, wiki_title=chapter.redmine_wiki, chapter=chapter)
            if categories:
                for category in categories:
                    tests = Test.objects.filter(category=category).order_by('id')
                    for test in tests:
                        if test.redmine_wiki:
                            redmine_test = RedmineTest()
                            configs = TestConfig.objects.filter(test=test).order_by('id')
                            images = TestImage.objects.filter(test=test).order_by('id')
                            files = TestFile.objects.filter(test=test).order_by('id')
                            checklists = TestChecklist.objects.filter(test=test).order_by('id')
                            links = TestLink.objects.filter(test=test).order_by('id')
                            comments = TestComment.objects.filter(test=test).order_by('id')
                            redmine_test.export(project=test.category.testplan.redmine_project,
                                                wiki_title=test.redmine_wiki, name=test.name, purpose=test.purpose,
                                                procedure=test.procedure, configs=configs, images=images, files=files,
                                                expected=test.expected, checklists=checklists, links=links,
                                                comments=comments)
        else:
            return redmine_project
        return is_wiki

    def parse_chapters_items(self):
        chapters = []
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Общие положения\r', h2_block)
            if detect_head:
                chapter_blocks = h2_block.split('\r\n* ')
                chapter_blocks.pop(0)
                for chapter_block in chapter_blocks:
                    detect_wiki = re.search(']]', chapter_block)
                    if detect_wiki:
                        wiki_title = chapter_block.split('|')[0][2:]
                        chapter_name = chapter_block.split('|')[1][:-2].replace(']', '')
                    else:
                        wiki_title = None
                        chapter_name = chapter_block.replace('\r', '').replace('\n', '')
                    chapter = {'redmine_wiki': wiki_title, 'name': chapter_name, 'text': None}
                    chapters.append(chapter)
        return chapters

    def parse_tests_items(self):
        categories = []
        for h2_block in self.wiki.split('\nh2. '):
            detect_head = re.search('Список тестов\r', h2_block)
            if detect_head:
                h3_blocks = h2_block.split('\nh3. ')
                del h3_blocks[0]
                for h3_block in h3_blocks:
                    category_name = h3_block.split('\r\n\r\n')[0]
                    test_blocks = h3_block.split('* ')
                    del test_blocks[0]
                    tests = []
                    for test_block in test_blocks:
                        detect_wiki = re.search(']]', test_block)
                        if detect_wiki:
                            redmine_wiki = test_block.split('|')[0][2:]
                            test_name = test_block.split('|')[1].replace(']', '').replace('\r', '').replace('\n', '')
                        else:
                            redmine_wiki = None
                            test_name = test_block.replace('\r', '').replace('\n', '')
                        test = {'redmine_wiki': redmine_wiki, 'name': test_name, 'purpose': None, 'procedure': None,
                                'configs': None, 'images': None, 'files': None, 'expected': None,
                                'checklists': None, 'links': None, 'comments': None}
                        tests.append(test)
                    category = {'name': category_name, 'tests': tests}
                    categories.append(category)
        return categories

    def parse_details(self, project: str, is_chapters, is_tests):
        is_wiki = RedmineProject().check_wiki(project=project, wiki_title='Wiki')
        if is_wiki[0]:
            self.wiki = is_wiki[1]
        else:
            return is_wiki
        if is_chapters:
            chapters = self.parse_chapters_items()
            for chapter in chapters:
                if chapter['redmine_wiki']:
                    is_wiki = RedmineChapter().parse_details(project=project, wiki_title=chapter['redmine_wiki'])
                    if is_wiki[0]:
                        chapter['text'] = is_wiki[1]['text']
        else:
            chapters = None
        if is_tests:
            categories = self.parse_tests_items()
            for category in categories:
                tests = category['tests']
                for test in tests:
                    if test['redmine_wiki']:
                        is_wiki = RedmineTest().parse_details(project=project, wiki_title=test['redmine_wiki'],
                                                              is_purpose=True, is_procedure=True, is_configs=True,
                                                              is_images=True, is_files=True, is_expected=True,
                                                              is_checklists=True, is_links=True, is_comments=True)
                        if is_wiki[0]:
                            test['purpose'] = is_wiki[1]['purpose']
                            test['procedure'] = is_wiki[1]['procedure']
                            test['configs'] = is_wiki[1]['configs']
                            test['images'] = is_wiki[1]['images']
                            test['files'] = is_wiki[1]['files']
                            test['expected'] = is_wiki[1]['expected']
                            test['checklists'] = is_wiki[1]['checklists']
                            test['links'] = is_wiki[1]['links']
                            test['comments'] = is_wiki[1]['comments']
        else:
            categories = None
        return [True, {'chapters': chapters, 'categories': categories}]


class RedmineFeatureList(object):
    def __init__(self):
        self.wiki = ''
        self.ctx = ''

    def get_wiki_feature_list(self, fl: FeatureList):
        self.ctx = 'h1. ' + fl.name + '\r\n\r'
        categories = FeatureListCategory.objects.filter(feature_list=fl).order_by('id')
        for category in categories:
            self.ctx += '\nh2. ' + category.name + '\r\n\r'
            items = FeatureListItem.objects.filter(category=category).order_by('id')
            for item in items:
                self.ctx += '\n** ' + item.name
                if item.optional:
                    self.ctx += ' %{color:red}(опционально)%'
                self.ctx += '\r'
            self.ctx += '\n\r'
        return self.ctx

    def export(self, project: str, wiki_title: str, fl: FeatureList):
        self.wiki += self.get_wiki_feature_list(fl)
        is_wiki = RedmineProject().create_or_update_wiki(project=project, wiki_title=wiki_title, wiki_text=self.wiki,
                                                         parent_title='wiki')
        return is_wiki

    def parse_details(self, project: str, wiki_title: str):
        is_wiki = RedmineProject().check_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0]:
            self.wiki = is_wiki[1]
            h2_blocks = self.wiki.split('\nh2. ')
            feature_list = {'name': h2_blocks[0][4:-3], 'categories': []}
            del h2_blocks[0]
            for h2_block in h2_blocks:
                h2_items = h2_block.split('\r\n')
                category_name = h2_items[0]
                category = {'name': category_name, 'items': []}
                for h2_item in h2_items[2:-1]:
                    item_name = h2_item[3:]
                    detect_optional = re.search('(опционально)', item_name)
                    if detect_optional:
                        optional = True
                        item_name = item_name.replace(' %{color:red}(опционально)%', '')
                    else:
                        optional = False
                    item = {'name': item_name, 'optional': optional}
                    category['items'].append(item)
                feature_list['categories'].append(category)
            return [True, feature_list]
        else:
            return [False, is_wiki[1]]


def get_wiki_device_type_specs(device_type: DeviceType):
    specs = DeviceTypeSpecification.objects.filter(type=device_type).order_by('id')
    if specs:
        ctx = '\nh2. Спецификации\r\n\r'
        for spec in specs:
            ctx += '\nh3. ' + spec.get_type() + '\r\n\r'
        return ctx
    else:
        return None


def get_wiki_device_type_tech_reqs(device_type: DeviceType):
    tech_reqs = FeatureList.objects.filter(device_type=device_type).order_by('id')
    if tech_reqs:
        ctx = '\nh2. Технические требования\r\n\r'
        for tech_req in tech_reqs:
            ctx += '\n* [[tech_req_' + str(tech_req.id) + '|' + tech_req.name + ']]\r\n\r'
        return ctx
    else:
        return None


class RedmineDeviceType:
    wiki: str

    def export(self, parent: str, project: str, project_name: str, device_type: DeviceType, specs: bool,
               tech_reqs: bool):
        r = RedmineProject()
        redmine_project = r.create_or_update_project(parent=parent, project=project, project_name=project_name)
        if not redmine_project[0]:
            return redmine_project
        else:
            # build wiki
            self.wiki = 'h1. ' + project_name + '\r\n\r\n'
            if specs:
                self.wiki += get_wiki_device_type_specs(device_type)
            if tech_reqs:
                self.wiki += get_wiki_device_type_tech_reqs(device_type)
            is_wiki = r.create_or_update_wiki(project=project, wiki_title='Wiki', wiki_text=self.wiki)
            return is_wiki
