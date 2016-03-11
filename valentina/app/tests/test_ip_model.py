from django.contrib.auth.models import User
from django.test import TestCase
from valentina.app.models import Ip


class TestIpModel(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        Ip.objects.create(user=User.objects.first(), address='0.0.0.0')

    def test_create(self):
        self.assertTrue(Ip.objects.exists())

    def test_srt(self):
        ip = Ip.objects.first()
        self.assertEqual('0.0.0.0', ip.address)
