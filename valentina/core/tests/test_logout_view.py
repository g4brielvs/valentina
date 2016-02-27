from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase


class TestGetLogout(TestCase):

    def setUp(self):
        User.objects.create_user('olivia', password='password')
        self.client.login(username='olivia', password='password')
        self.resp = self.client.get(resolve_url('logout'))

    def test_get(self):
        self.assertRedirects(self.resp, resolve_url('home'))
