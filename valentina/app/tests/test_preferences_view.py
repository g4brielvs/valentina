from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation


class TestGet(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # create user with password and affiliate her to an inactive chatroom
        self.user = User.objects.create_user('valentinavc',
                                             password='valentina')
        self.chat = Chat.objects.first()
        profile_data = {'user': self.user,
                        'gender': Profile.FEMALE,
                        'nickname': 'Olivia'}
        Profile.objects.create(**profile_data)
        self.affiliation = Affiliation.objects.create(chat=self.chat,
                                                      user=self.user,
                                                      alias='Geek',
                                                      active=False)

        # login
        self.login = self.client.login(username='valentinavc',
                                       password='valentina')
        data = {'key': self.affiliation.hash_id, 'active': True}
        self.resp = self.client.post(resolve_url('app:preferences'), data=data,
                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_post(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_affiliation_active_status_changed(self):
        json_resp = self.resp.json()
        self.assertTrue(json_resp['active'])
