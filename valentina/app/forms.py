from django import forms
from valentina.app.models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content', 'chat']
