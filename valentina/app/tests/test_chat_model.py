from django.test import TestCase
from valentina.app.models import Chat


class TestChatModel(TestCase):

    def setUp(self):
        self.chat = Chat.objects.create(person='42')

    def test_create(self):
        self.assertTrue(Chat.objects.exists())

    def test_srt(self):
        self.assertEqual('42', self.chat.person)

    def test_encode_hash_id(self):
        hash_id = self.chat.hash_id
        with self.subTest():
            self.assertTrue(hash_id)
            self.assertNotEqual(1, hash_id)
            self.assertEqual(1, Chat.get_id_from_hash(hash_id))
