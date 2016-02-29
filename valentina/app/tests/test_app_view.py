from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile


class TestGetApp(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('olivia', password='password')
        Profile.objects.create(gender=Profile.FEMALE, user=self.user)


class TestGetWithFemaleUserAuthenticated(TestGetApp):

    def setUp(self):
        super().setUp()
        self.client.login(username='olivia', password='password')
        self.resp = self.client.get(resolve_url('app:welcome'))

    def test_get_for_female_user(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'app/home.html')

    def test_logout_link(self):
        url = resolve_url('app:logout')
        expected = 'href="{}"'.format(url)
        self.assertContains(self.resp, expected)


class TestGetAppWithMaleUser(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('stan', password='password')
        Profile.objects.create(gender=Profile.MALE, user=self.user)


class TestGetWithMaleUserAuthenticated(TestGetAppWithMaleUser):

    def test_get_for_male_user(self):
        self.client.login(username='stan', password='password')
        resp = self.client.get(resolve_url('app:welcome'))
        self.assertRedirects(resp, resolve_url('female_only'))

    def test_get_for_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='stan', password='password')
        resp = self.client.get(resolve_url('app:welcome'))
        self.assertEqual(200, resp.status_code)


class TestGetWithoutUserAuthenticated(TestGetApp):

    def setUp(self):
        super().setUp()
        self.client.login(username='stan', password='password')
        self.resp = self.client.get(resolve_url('app:welcome'))

    def test_get(self):
        home_url = resolve_url('home')
        app_url = resolve_url('app:welcome')
        expected = '{}?next={}'.format(home_url, app_url)
        self.assertRedirects(self.resp, expected)
