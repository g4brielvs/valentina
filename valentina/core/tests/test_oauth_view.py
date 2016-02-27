from django.test import TestCase


class TestOAuthGet(TestCase):

    def test_get(self):
        resp = self.client.get('/oauth/login/facebook/')
        self.assertEqual(302, resp.status_code)
