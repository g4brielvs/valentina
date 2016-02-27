from django.shortcuts import resolve_url
from django.test import TestCase


class TestGetApp(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('app'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)
