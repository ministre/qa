from redminelib import Redmine
from qa import settings
from redminelib.exceptions import ResourceNotFoundError, ForbiddenError, AuthError
from requests.exceptions import ConnectionError


class RedmineProject(object):

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.0.4')

    def get_wiki_url(self):
        try:
            self.redmine.wiki_page.get('Wiki', project_id=self.project_id)
            return [True, settings.REDMINE_URL + '/projects/' + self.project_id + '/wiki/']
        except ConnectionError:
            return [False, 'Connection Error']
        except ResourceNotFoundError:
            return [False, 'Not found']
        except ForbiddenError:
            return [False, 'Requested resource is forbidden']
        except AuthError:
            return [False, 'Authentication Error']
