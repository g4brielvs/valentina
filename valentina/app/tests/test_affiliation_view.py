from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation


class TestAffiliation(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # create user with password and affiliate her to a chatroom
        self.user = User.objects.create_user('joane', password='joane')
        data = {'user': self.user, 'nickname': 'doe', 'gender': Profile.FEMALE}
        Profile.objects.create(**data)

        # login and POST
        self.login = self.client.login(username='joane', password='joane')
        self.data = {'person': 'stan_id', 'alias': 'Geek'}
        self.ajax = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = resolve_url('app:affiliation')
        self.resp = self.client.post(url, data=self.data, **self.ajax)


class TestPost(TestAffiliation):

    def test_post(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(201, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        chat = Chat.objects.first()
        chat_url = resolve_url('app:chat', chat.hash_id)
        affiliation = chat.affiliation_set.filter(user=self.user).first()
        with self.subTest():
            self.assertEqual(json_resp['url'], chat_url)
            self.assertEqual(json_resp['key'], affiliation.hash_id)
            self.assertEqual(json_resp['alias'], 'Geek')
            self.assertEqual(json_resp['active'], True)
            self.assertEqual(json_resp['valentinas'], 3)

    def test_affiliation_exists(self):
        self.assertTrue(Affiliation.objects.filter(user=self.user).exists())


class TestGet(TestAffiliation):

    def setUp(self):
        super().setUp()
        url = resolve_url('app:affiliations')
        self.resp = self.client.get(url, **self.ajax)

    def test_get(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        chat = Chat.objects.first()
        chat_url = resolve_url('app:chat', chat.hash_id)
        affiliation = chat.affiliation_set.filter(user=self.user).first()
        with self.subTest():
            self.assertEqual(1, len(json_resp['chats']))
            self.assertEqual(json_resp['chats'][0]['url'], chat_url)
            self.assertEqual(json_resp['chats'][0]['key'], affiliation.hash_id)
            self.assertEqual(json_resp['chats'][0]['alias'], 'Geek')
            self.assertEqual(json_resp['chats'][0]['active'], True)
            self.assertEqual(json_resp['chats'][0]['valentinas'], 3)

    def test_affiliation_exists(self):
        self.assertTrue(Affiliation.objects.filter(user=self.user).exists())
