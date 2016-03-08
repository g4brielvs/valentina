import arrow
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from valentina.app.facebook import GetFacebookData
from valentina.app.forms import (MessageForm, ProfileForm, FacebookSearchForm,
                                 ReportForm, AffiliationForm)
from valentina.app.models import Profile, Chat, Message, Affiliation, Report


@login_required(login_url='/')
def welcome(request):

    # abort if request has no user
    if not request.user:
        return redirect(resolve_url('home'))

    # abort if user is not valid
    if not _valid_user(request.user):
        return redirect(resolve_url('female_only'))

    # suggest random nickname for new users
    profile = request.user.profile
    nickname = profile.nickname
    random_nickname = profile.create_nickname() if not nickname else None

    context = {'chats': _affiliations_to_ctx(request.user),
               'nickname': nickname, 'random_nickname': random_nickname}

    return render(request, 'app/home.html', context)


@login_required(login_url='/')
def chat(request, pk):
    if request.is_ajax():
        if request.method == 'POST':
            return save_message(request, pk)
        if request.method == 'GET':
            return list_messages(request, pk)
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required(login_url='/')
def list_messages(request, pk):

    chat = get_object_or_404(Chat, pk=pk)
    affiliation = get_object_or_404(Affiliation, chat=chat, user=request.user)
    messages = Message.objects.filter(chat=chat)[:50]

    chat_details = {'id': chat.pk, 'alias': affiliation.alias}
    messages = [_message_to_dict(request, msg) for msg in messages]

    return JsonResponse({'chat': chat_details, 'messages': messages})


@login_required(login_url='/')
def save_message(request, pk):

    form = MessageForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors}, status=400)

    chat = Chat.objects.get(pk=pk)
    if not chat:
        return JsonResponse({'error': 'Invalid chat'}, status=401)

    affiliation = Affiliation.objects.filter(chat=chat, user=request.user)
    if not affiliation:
        return JsonResponse({'error': 'User does not belongs to chat'},
                            status=401)

    message = Message.objects.create(chat=chat, user=request.user,
                                     content=form.cleaned_data.get('content'))

    return JsonResponse(_message_to_dict(request, message), status=201)


@login_required(login_url='/')
def profile(request):

    if request.method == 'POST' and request.is_ajax():
        form = ProfileForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname')
            request.user.profile.nickname = nickname
            request.user.profile.save()
            return JsonResponse({'nickname': nickname})
        else:
            return JsonResponse({'error': form.errors}, status=400)

    return HttpResponseNotAllowed(['POST'])


@login_required(login_url='/')
def facebook(request):

    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseNotAllowed(['POST'])

    form = FacebookSearchForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': 'URL inválida.'})

    token = _get_token(request.user)
    person = GetFacebookData(form.cleaned_data.get('url'), token=token)

    return JsonResponse(person.data)


@login_required(login_url='/')
def affiliation(request):

    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseNotAllowed(['POST'])

    form = AffiliationForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors})

    alias = form.cleaned_data.get('alias')
    chat, created = Chat.objects.get_or_create(person=form.cleaned_data.get('person'))
    affiliation = Affiliation.objects.filter(chat=chat, user=request.user).first()
    if affiliation:
        affiliation.alias = alias
        affiliation.save()
    else:
        affiliation = Affiliation.objects.create(chat=chat, user=request.user,
                                                 alias=alias)

    return JsonResponse(_affiliation_to_dict(affiliation))


@login_required(login_url='/')
def report(request):

    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseNotAllowed(['POST'])

    form = ReportForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors})

    message = get_object_or_404(Message, pk=form.cleaned_data.get('pk'))
    report = Report.objects.create(message=message, user=request.user)
    return JsonResponse({'report': report.pk}, status=201)


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


def _get_token(user):

    # use APP_TOKEN if user is staff
    if user.is_staff:
        return settings.FACEBOOK_APP_TOKEN

    # use USER_TOKEN otherwise
    if hasattr(user, 'profile'):
        return user.profile.access_token


def _message_to_dict(request, message):
    created_at = arrow.get(message.created_at)
    css_class = 'me' if request.user == message.user else ''
    return {'content': message.content,
            'ago': created_at.humanize(locale=settings.LANGUAGE_CODE[:2]),
            'author': message.user.profile.nickname,
            'id': message.pk,
            'className': css_class}


def _affiliations_to_ctx(user):
    output = list()
    for affiliation in Affiliation.objects.filter(user=user):
        output.append(_affiliation_to_dict(affiliation))
    return output


def _affiliation_to_dict(affiliation):
    return dict(url=resolve_url('app:chat', affiliation.chat.pk),
                alias=affiliation.alias,
                valentinas=affiliation.chat.affiliation_set.count())
