from django.test import TestCase

from valentina.app.forms import MessageForm


class MessageFormtest(TestCase):

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = MessageForm()
        self.assertSequenceEqual(list(form.fields), ['content', 'chat'])
