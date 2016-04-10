from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation


class TestPost(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # create user with password and affiliate her to a chatroom
        self.user = User.objects.create_user('joane', password='joane')
        data = {'user': self.user, 'nickname': 'doe', 'gender': Profile.FEMALE}
        Profile.objects.create(**data)

        # login and GET
        self.login = self.client.login(username='joane', password='joane')
        data = {'person': 'stan_id', 'alias': 'Geek'}
        url = resolve_url('app:affiliation')
        ajax = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.resp = self.client.post(url, data=data, **ajax)

    def test_post(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(201, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        chat = Chat.objects.first()
        chat_url = resolve_url('app:chat', chat.pk)
        with self.subTest():
            self.assertEqual(json_resp['url'], chat_url)
            self.assertEqual(json_resp['alias'], 'Geek')
            self.assertEqual(json_resp['valentinas'], 3)

    def test_affiliation_exists(self):
        self.assertTrue(Affiliation.objects.filter(user=self.user).exists())