from django.test import TestCase
from valentina.app.forms import FacebookSearchForm


class TestForm(TestCase):

    def test_form_has_fields(self):
        form = FacebookSearchForm()
        self.assertSequenceEqual(list(form.fields), ['url'])
