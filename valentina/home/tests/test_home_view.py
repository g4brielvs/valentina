from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url
from valentina.app.models import Profile


class TestGetHomeWithoutUserAuthenticated(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'home/home.html')

    def test_login_link(self):
        expected = 'href="{}"'.format('/oauth/login/facebook/')
        self.assertContains(self.resp, expected)


class TestGetHomeWithUserAuthenticated(TestCase):

    def test_get(self):
        user = User.objects.create_user('olivia', password='password')
        self.client.login(username='olivia', password='password')
        Profile.objects.create(gender=Profile.FEMALE, user=user)
        resp = self.client.get(resolve_url('home'))
        self.assertRedirects(resp, resolve_url('app:welcome'))
