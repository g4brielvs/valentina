from django.test import TestCase
from valentina.app.models import Chat


class TestChatModel(TestCase):

    def setUp(self):
        Chat.objects.create(person='42')

    def test_create(self):
        self.assertTrue(Chat.objects.exists())

    def test_srt(self):
        chat = Chat.objects.first()
        self.assertEqual('42', chat.person)
