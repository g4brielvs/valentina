from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation, Message


class TestCaseAPI(TestCase):

    """
    This is basic test case for all API methods that are called within the chat
    page. It tests all request methods (and many possibilities reagrding user
    authentication) that should be denied (405, 422, 302 to login/home page).

    It does NOT test any success case (as they may very too much, such as 200
    for GET, 201 for POST for example).

    It does NOT test data validation either (as it also varies too much).
    """

    USERNAME = 'valentinavc'
    PASSWORD = 'valentinavc'
    NICKNAME = 'joane doe'
    CHAT_ALIAS = 'Geek'

    MALE = 'stan'
    OTHER = 'other'
    BLOCKED = 'hammer'

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # handle user and chat database objects
        user_data = {'password': self.PASSWORD}
        self.user = User.objects.create_user(self.USERNAME, **user_data)
        self.chat = Chat.objects.first()
        profile_data = {'user': self.user, 'nickname': self.NICKNAME,
                        'gender': Profile.FEMALE}
        self.profile = Profile.objects.create(**profile_data)
        affiliation_data = {'chat': self.chat, 'user': self.user,
                            'alias': self.CHAT_ALIAS}
        self.affiliation = Affiliation.objects.create(**affiliation_data)
        self.message = Message.objects.first()

        # list all URLs, their allowed methods, and the required data
        self.cases = ({'url': resolve_url('app:chat', self.chat.hash_id),
                       'allowed_methods': ('get', 'post'),
                       'data': {'content': 'Hey', 'chat': self.chat.hash_id}},
                      {'url': resolve_url('app:profile'),
                       'allowed_methods': ('post'),
                       'data': {'nickname': 'Olivia'}},
                      {'url': resolve_url('app:affiliation'),
                       'allowed_methods': ('post'),
                       'data': {'alias': 'Guy', 'person': '4'}},
                      {'url': resolve_url('app:report'),
                       'allowed_methods': ('post'),
                       'data': {'pk': self.message.hash_id}})

        # set main vars for HTTP request tests
        self.ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.methods = {'get': self.client.get,
                        'post': self.client.post,
                        'put': self.client.put,
                        'patch': self.client.patch,
                        'delete': self.client.delete}

    def get_all_requests(self, credentials=None):
        """Loops through cases and yields all required HTTP responses"""

        # loop cases
        cases = list()
        for case in self.cases:

            # get case info
            url = case.get('url')
            data = case.get('data')
            allowed_methods = case.get('allowed_methods')

            # run the requests
            for method_name, method in self.methods.items():

                # skip data if not post
                case_data = data if method_name == 'post' else None

                # login & request (standard)
                if credentials:
                    self.client.login(**credentials)
                resp = method(url, data=case_data)
                cases.append((url, method_name, allowed_methods, resp, False))

                # login & request (ajax)
                if credentials:
                    self.client.login(**credentials)
                ajax = method(url, data=case_data, **self.ajax_header)
                cases.append((url, method_name, allowed_methods, ajax, True))

        return cases

    def create_alternative_user(self, username, gender):
        user = User.objects.create_user(username, password=username)
        Profile.objects.create(user=user, gender=gender)
        affiliation_data = {'chat': self.chat, 'user': user, 'alias': 'Geek'}
        Affiliation.objects.create(**affiliation_data)

    def test_requests_without_login(self):
        """
        All methods should redirect to login page when user is not logged in
        """
        requests = self.get_all_requests()
        for url, method, allowed, resp, ajax in requests:
            with self.subTest():
                expected = '{}?next={}'.format(resolve_url('home'), url)
                self.assertRedirects(resp, expected)

    def test_requests_with_login(self):
        """
        All not allowed methods should return 405 status code with ajax, or
        422 without ajax
        """
        credentials = {'username': self.USERNAME, 'password': self.PASSWORD}
        requests = self.get_all_requests(credentials)
        for url, method, allowed, resp, ajax in requests:
            with self.subTest():
                if not ajax:
                    self.assertEqual(422, resp.status_code)
                elif method not in allowed:
                    self.assertEqual(405, resp.status_code)

    def test_male_user(self):
        """All requests by male users should return 403"""
        self.create_alternative_user(self.MALE, Profile.MALE)
        credentials = {'username': self.MALE, 'password': self.MALE}
        requests = self.get_all_requests(credentials)
        for url, method, allowed, resp, ajax in requests:
            with self.subTest():
                self.assertEqual(403, resp.status_code)

    def test_other_user(self):
        """All requests by other gender users should return 403"""
        self.create_alternative_user(self.OTHER, Profile.OTHER)
        credentials = {'username': self.OTHER, 'password': self.OTHER}
        requests = self.get_all_requests(credentials)
        for url, method, allowed, resp, ajax in requests:
            with self.subTest():
                self.assertEqual(403, resp.status_code)

    def test_blocked_user(self):
        """All requests by blocked users should return 403"""
        self.user.profile.blocked = True
        self.user.profile.save()
        credentials = {'username': self.USERNAME, 'password': self.PASSWORD}
        requests = self.get_all_requests(credentials)
        for url, method, allowed, resp, ajax in requests:
            with self.subTest():
                self.assertEqual(403, resp.status_code)
