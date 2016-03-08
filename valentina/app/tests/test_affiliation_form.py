from django.test import TestCase
from valentina.app.forms import AffiliationForm


class TestForm(TestCase):

    def test_form_has_fields(self):
        form = AffiliationForm()
        self.assertSequenceEqual(list(form.fields), ['person', 'alias'])
