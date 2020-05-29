from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError, ValidationError
from requests.exceptions import ConnectionError
from testplan.models import TestChecklistItem
import re


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

    def create_or_update_project(self, project: str, project_name: str, parent=''):
        is_project = self.check_project(project=project)
        if is_project[0]:
            # update project
            self.redmine.project.update(resource_id=is_project[1], name=project_name)
            return [True, 'Project updated']
        else:
            if is_project[1] == 'Project not found':
                if parent:
                    is_parent_project = self.check_project(project=parent)
                    if is_parent_project[0]:
                        # create sub-project
                        try:
                            p = self.redmine.project.create(identifier=project, name=project_name,
                                                            parent_id=is_parent_project[1], inherit_members=True)
                            return [True, p.id]
                        except ValidationError:
                            return [False, 'Sub-project name validation error']
                    else:
                        if is_parent_project[1] == 'Project not found':
                            return [False, 'Parent project not found']
                        else:
                            return [False, 'Parent project error - ' + is_parent_project[1]]
                else:
                    # create root project
                    try:
                        p = self.redmine.project.create(identifier=project, name=project_name, inherit_members=True)
                        return [True, p.id]
                    except ValidationError:
                        return [False, 'Root project name validation error']
            else:
                return [False, is_project[1]]

    def create_or_update_wiki(self, project: str, wiki_title: str, wiki_text: str):
        is_wiki = self.check_wiki(project=project, wiki_title=wiki_title)
        if is_wiki[0]:
            self.redmine.wiki_page.update(wiki_title, project_id=project, text=wiki_text)
            return [True, 'Wiki updated']
        else:
            if is_wiki[1] == 'Wiki not found':
                self.redmine.wiki_page.create(project_id=project, title=wiki_title, text=wiki_text, parent_title='wiki')
                return [True, 'Wiki created']
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
                h3_blocks = h2_block.split('\nh3. ')
                procedure_blocks = h3_blocks[0].split('\n')
                procedure = procedure_blocks[2][:-1]
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
                checklist_items = TestChecklistItem.objects.filter(checklist=checklist)
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

        wiki_page = RedmineProject().create_or_update_wiki(project=project, wiki_title=wiki_title, wiki_text=self.wiki)
        return wiki_page


class RedmineTestPlan(object):
    def __init__(self):
        pass
