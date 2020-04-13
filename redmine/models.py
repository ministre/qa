from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError
from requests.exceptions import ConnectionError
from device.models import DeviceType


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

    def get_wiki_url(self):
        if self.get_project()[0]:
            try:
                self.redmine.wiki_page.get('Wiki', project_id=self.project_id)
                return [True, settings.REDMINE_URL + '/projects/' + self.project_id + '/wiki/']
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
