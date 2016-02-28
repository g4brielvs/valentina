from django.test import TestCase
from django.shortcuts import resolve_url


class TestGetBlocked(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('blocked'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'home/blocked.html')
