import json
import re
import requests


class GetFacebookData(object):

    TYPES = {'user': 'pessoa', 'page': 'página', 'group': 'Grupo',
             'event': 'evento', 'application': 'aplicativo'}
    INVALID_URL = """Desculpe, mas a URL digitada não parece de um perfil de
                     uma pessoa no Facebook."""
    API_URL = 'https://graph.facebook.com'

    def __init__(self, url=None, token=None):
        self.url = url
        self.token = token
        self.facebook_id = self.find_id()
        self.data = self.load_facebook_data()

    def find_id(self, contents=None):

        contents = self._load_url() if not contents else contents
        if not contents:
            return False

        pattern = r'(entity_id["\' ]{1,3}:["\' ]{1,3})([\d]+)'
        regex = re.compile(pattern, flags=re.VERBOSE)
        match = regex.search(contents)

        try:
            return match.group(2)
        except (IndexError, AttributeError):
            return False

    def load_facebook_data(self, facebook_id=None):

        facebook_id = self.facebook_id if not facebook_id else facebook_id
        if not facebook_id:
            return {'error': self.INVALID_URL}

        query = {'metadata': 1, 'access_token': self.token,
                 'fields': 'id,name,link,picture.width(720).height(720)'}
        url = '{}/{}'.format(self.API_URL, facebook_id)
        response = self._load_url(url, params=query)

        if not response:
            return {'error': self.INVALID_URL}

        data = json.loads(response)
        try:
            picture = data['picture']['data']['url']
        except KeyError:
            picture = None
        try:
            type_ = self.TYPES.get(data['metadata']['type'], 'desconhecido')
        except KeyError:
            type_ = None

        return {'id': data.get('id'),
                'name': data.get('name'),
                'picture': picture,
                'link': data.get('link'),
                'type': type_}

    def _load_url(self, url=None, **kwargs):
        url = self.url if not url else url
        resp = requests.get(url, params=kwargs.get('params'))
        if resp.status_code != 200:
            print('HTTP status {} ({})'.format(resp.status_code, url))
            return None
        return resp.text
