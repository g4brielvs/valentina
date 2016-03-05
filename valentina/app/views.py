import arrow
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.conf import settings
from valentina.app.models import Profile, Chat, Message, Affiliation


@login_required(login_url='/')
def welcome(request):

    # abort if request has no user
    if not request.user:
        return redirect(resolve_url('home'))

    # abort if user is not valid
    if not _valid_user(request.user):
        return redirect(resolve_url('female_only'))

    return render(request, 'app/home.html')


@login_required(login_url='/')
def chat(request, pk):

    chat = get_object_or_404(Chat, pk=pk)
    affiliation = get_object_or_404(Affiliation, chat=chat, user=request.user)
    messages = Message.objects.filter(chat=chat)[:50]

    contents = {'chat_id': chat.pk,
                'chat_alias': affiliation.alias,
                'messages': [_message_to_dict(msg) for msg in messages]}

    return JsonResponse(contents)


def logout(request):
    auth_logout(request)
    return redirect(resolve_url('home'))


def _valid_user(user):

    # authorize if user is staff
    if user.is_staff:
        return True

    # authorize if user is female
    if hasattr(user, 'profile'):
        if user.profile.gender == Profile.FEMALE:
            return True

    return False


def _message_to_dict(message):
    created_at = arrow.get(message.created_at)
    return {'content': message.content,
            'ago': created_at.humanize(locale=settings.LANGUAGE_CODE[:2]),
            'author': message.user.profile.nickname,
            'id': message.pk}
