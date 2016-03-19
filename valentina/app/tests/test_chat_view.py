from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation, Message


class TestGet(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # create user with password and affiliate her to a chatroom
        self.user = User.objects.create_user('valentinavc',
                                             password='valentina')
        self.chat = Chat.objects.first()
        profile_data = {'user': self.user,
                        'gender': Profile.FEMALE,
                        'nickname': 'Olivia'}
        Profile.objects.create(**profile_data)
        self.affiliation = Affiliation.objects.create(chat=self.chat,
                                                      user=self.user,
                                                      alias='Geek')

        # login and GET
        self.login = self.client.login(username='valentinavc',
                                       password='valentina')
        self.resp = self.client.get(resolve_url('app:chat', self.chat.pk),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_get(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents_no_previous_messages(self):
        """Once user joins a chat, she should not see previous messages"""
        json_resp = self.resp.json()
        with self.subTest():
            self.assertEqual(json_resp['chat']['id'], self.chat.pk)
            self.assertEqual(json_resp['chat']['alias'], 'Geek')
            self.assertEqual(0, len(json_resp['messages']))

    def test_contents_new_messages(self):
        """Once user joins a chat, she should see new messages only"""

        # test user says hi and others reply
        Message.objects.create(user=self.user, chat=self.chat, content='Hi')
        Message.objects.create(user=User.objects.get(pk=1),
                               chat=self.chat, content='Hi')
        Message.objects.create(user=User.objects.get(pk=2),
                               chat=self.chat, content='Hi')
        resp = self.client.get(resolve_url('app:chat', self.chat.pk),
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        json_resp = resp.json()
        with self.subTest():
            self.assertEqual(json_resp['chat']['id'], self.chat.pk)
            self.assertEqual(json_resp['chat']['alias'], 'Geek')
            self.assertEqual(json_resp['chat']['user'], 'Olivia')
            self.assertEqual(3, len(json_resp['messages']))


class TestPost(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # create user with password and affiliate her to a chatroom
        self.user = User.objects.create_user('valentinavc', password='valentina')
        self.chat = Chat.objects.first()
        Profile.objects.create(user=self.user, gender=Profile.FEMALE, nickname='valanon')
        Affiliation.objects.create(chat=self.chat, user=self.user, alias='Geek')

        # login and POST
        self.login = self.client.login(username='valentinavc',
                                       password='valentina')
        data = {'content': 'Hello, world', 'chat': self.chat.pk}
        self.resp = self.client.post(resolve_url('app:chat', self.chat.pk),
                                     data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_post(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(201, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        with self.subTest():
            self.assertEqual(json_resp['content'], 'Hello, world')
            self.assertEqual(json_resp['ago'], 'agora')
            self.assertEqual(json_resp['author'], 'valanon')
            self.assertEqual(json_resp['className'], 'me')

    def test_message_count_increased(self):
        self.assertEqual(3, Message.objects.filter(chat=self.chat).count())
