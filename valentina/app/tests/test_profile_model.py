from django.contrib.auth.models import User
from django.test import TestCase
from valentina.app.models import Profile


class TestProfileModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('olivia')

    def test_create(self):
        Profile.objects.create(gender=Profile.FEMALE, timezone='-3',
                               nickname='palito', user=self.user)
        self.assertTrue(Profile.objects.exists())
