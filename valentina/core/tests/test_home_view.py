from django.test import TestCase
from django.shortcuts import resolve_url

from unittest import skip


class TestGetHome(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'home.html')

    @skip('next step')
    def test_login_link(self):
        expected = 'href="{}"'.format(resolve_url('login'))
        self.assertContains(self.resp, expected)
