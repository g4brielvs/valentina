from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from valentina.app.models import Profile


class TestGetHomeWithoutUserAuthenticated(TestCase):

    def setUp(self):
        self.resp = self.client.get(reverse('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'home/home.html')

    def test_login_link(self):
        url = reverse('oauth:begin', kwargs={'backend': 'facebook'})
        expected = 'href="{}"'.format(url)
        self.assertContains(self.resp, expected)


class TestGetHomeWithUserAuthenticated(TestCase):

    def test_get(self):
        user = User.objects.create_user('olivia', password='password')
        self.client.login(username='olivia', password='password')
        Profile.objects.create(gender=Profile.FEMALE, user=user)
        resp = self.client.get(reverse('home'))
        self.assertRedirects(resp, reverse('app:welcome'))
