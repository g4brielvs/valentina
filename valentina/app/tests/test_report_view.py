from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile


class TestProfile(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):
        self.user = User.objects.create_user('valentinavc', password='valentinavc')
        Profile.objects.create(user=self.user, gender=Profile.FEMALE, nickname='fulana')

    def test_get_without_login(self):
        resp = self.client.get(resolve_url('app:report'))
        self.assertEqual(302, resp.status_code)

    def test_get_with_login(self):
        self.login = self.client.login(username='valentinavc', password='valentinavc')
        resp = self.client.get(resolve_url('app:report'))
        self.assertEqual(405, resp.status_code)

    def test_post_with_login(self):
        self.login = self.client.login(username='valentinavc', password='valentinavc')
        resp = self.client.post(resolve_url('app:report'), {'pk': 1},
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(201, resp.status_code)
