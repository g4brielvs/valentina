from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Message


class TestProfile(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):
        self.user = User.objects.create_user('valentinavc', password='valentinavc')
        Profile.objects.create(user=self.user, gender=Profile.FEMALE, nickname='fulana')

    def test_post(self):
        self.login = self.client.login(username='valentinavc', password='valentinavc')
        hash_id = Message.objects.first().hash_id
        resp = self.client.post(resolve_url('app:report'), {'key': hash_id},
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(201, resp.status_code)
