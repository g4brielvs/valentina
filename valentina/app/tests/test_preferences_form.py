from django.test import TestCase

from valentina.app.forms import ChatPreferencesForm


class ChatPreferencesFormTest(TestCase):

    def test_form_has_fields(self):
        form = ChatPreferencesForm()
        self.assertSequenceEqual(list(form.fields), ['key', 'active'])
