from django.test import TestCase
from django.shortcuts import resolve_url


class TestGetHome(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'home.html')

    def test_login_link(self):
        expected = 'href="{}"'.format('/oauth/login/facebook/')
        self.assertContains(self.resp, expected)
