from django.core.urlresolvers import reverse
from django.test import TestCase


class TestOAuthGet(TestCase):

    def test_get(self):
        url = reverse('oauth:begin', kwargs={'backend': 'facebook'})
        resp = self.client.get(url)
        self.assertEqual(302, resp.status_code)
