from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase


class TestGetApp(TestCase):

    def setUp(self):
        User.objects.create_user('olivia', password='password')


class TestGetWithUserAuthenticated(TestGetApp):

    def setUp(self):
        super().setUp()
        self.client.login(username='olivia', password='password')
        self.resp = self.client.get(resolve_url('app'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)


class TestGetWithoutUserAuthenticated(TestGetApp):

    def setUp(self):
        super().setUp()
        self.client.login(username='stan', password='password')
        self.resp = self.client.get(resolve_url('app'))

    def test_get(self):
        home_url = resolve_url('home')
        app_url = resolve_url('app')
        expected = '{}?next={}'.format(home_url, app_url)
        self.assertRedirects(self.resp, expected)
