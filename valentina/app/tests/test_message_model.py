from django.contrib.auth.models import User
from django.test import TestCase
from valentina.app.models import Chat, Message


class TestMessageModel(TestCase):

    def setUp(self):
        self.chat = Chat.objects.create(person='42')
        self.user = User.objects.create_user(username='olivia')

    def test_create(self):
        Message.objects.create(chat=self.chat, user=self.user)
        self.assertTrue(Message.objects.exists())
