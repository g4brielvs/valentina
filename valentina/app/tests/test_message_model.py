from django.contrib.auth.models import User
from django.test import TestCase
from valentina.app.models import Chat, Message


class TestMessageModel(TestCase):

    def setUp(self):
        self.chat = Chat.objects.create(person='42')
        self.user = User.objects.create_user(username='olivia')
        self.message = Message.objects.create(chat=self.chat, user=self.user)

    def test_create(self):
        self.assertTrue(Message.objects.exists())

    def test_encode_hash_id(self):
        hash_id = self.message.hash_id
        with self.subTest():
            self.assertTrue(hash_id)
            self.assertNotEqual(1, hash_id)
            self.assertEqual(1, Message.get_id_from_hash(hash_id))
