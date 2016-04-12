import arrow
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import (JsonResponse, HttpResponse, HttpResponseForbidden,
                         HttpResponseNotAllowed)
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from valentina.app.facebook import GetFacebookData
from valentina.app.forms import (MessageForm, ProfileForm, FacebookSearchForm,
                                 ReportForm, AffiliationForm,
                                 ChatPreferencesForm)
from valentina.app.models import Profile, Chat, Message, Affiliation, Report


@login_required(login_url='/')
def welcome(request):

    # abort if invalid request
    should_abort = _should_abort(request, 'GET', ajax_only=False)
    if should_abort:
        return should_abort

    # suggest random nickname for new users
    profile = request.user.profile
    nickname = profile.nickname
    random_nickname = profile.create_nickname() if not nickname else None

    context = {'nickname': nickname, 'random_nickname': random_nickname}

    return render(request, 'app/home.html', context)


@login_required(login_url='/')
def chat(request, hash_id):

    # abort if invalid request
    should_abort = _should_abort(request, ['GET', 'POST'])
    if should_abort:
        return should_abort

    if request.method == 'POST':
        return save_message(request, Chat.get_id_from_hash(hash_id))

    if request.method == 'GET':
        return list_messages(request, Chat.get_id_from_hash(hash_id))


@login_required(login_url='/')
def list_messages(request, pk):

    chat = get_object_or_404(Chat, pk=pk)
    affiliation = get_object_or_404(Affiliation, chat=chat, user=request.user)
    msgs_filter = {'chat': chat, 'created_at__gt': affiliation.created_at}
    msgs = Message.objects.filter(**msgs_filter)[:50]

    chat_details = {'key': chat.hash_id,
                    'alias': affiliation.alias,
                    'user': request.user.profile.nickname}
    messages = [_message_to_dict(request, msg) for msg in msgs]

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
def chat_preferences(request):

    # abort if invalid request
    should_abort = _should_abort(request, ['POST'])
    if should_abort:
        return should_abort

    form = ChatPreferencesForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors}, status=400)

    pk = Affiliation.get_id_from_hash(form.cleaned_data.get('key'))
    affiliation = get_object_or_404(Affiliation, pk=pk, user=request.user)
    affiliation.active = form.cleaned_data.get('active')
    affiliation.save()
    return JsonResponse(_affiliation_to_dict(affiliation))


@login_required(login_url='/')
def profile(request):

    # abort if invalid request
    should_abort = _should_abort(request, 'POST')
    if should_abort:
        return should_abort

    form = ProfileForm(request.POST)
    if form.is_valid():
        nickname = form.cleaned_data.get('nickname')
        request.user.profile.nickname = nickname
        request.user.profile.save()
        return JsonResponse({'nickname': nickname})
    else:
        return JsonResponse({'error': form.errors}, status=400)


@login_required(login_url='/')
def facebook(request):

    # abort if invalid request
    should_abort = _should_abort(request, 'POST')
    if should_abort:
        return should_abort

    form = FacebookSearchForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': 'URL inválida.'})

    token = _get_token(request.user)
    person = GetFacebookData(form.cleaned_data.get('url'), token=token)

    # check if user already tagged this person
    chat = Chat.objects.filter(person=person.facebook_id).first()
    args = {'chat': chat, 'user': request.user}
    affiliation = Affiliation.objects.filter(**args).first()
    if affiliation:
        error = "Você já entrou na sala do(a) {} e a apelidou de “{}”."
        name = person.data.get('name')
        return JsonResponse({'error': error.format(name, affiliation.alias)})

    return JsonResponse(person.data)


@login_required(login_url='/')
def list_affiliations(request):

    # abort if invalid request
    should_abort = _should_abort(request, 'GET')
    if should_abort:
        return should_abort

    return JsonResponse(dict(chats=_affiliations_to_ctx(request.user)))


@login_required(login_url='/')
def create_affiliation(request):

    # abort if invalid request
    should_abort = _should_abort(request, 'POST')
    if should_abort:
        return should_abort

    form = AffiliationForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors})

    # make sure chat exists
    chat_data = {'person': form.cleaned_data.get('person')}
    chat, created = Chat.objects.get_or_create(**chat_data)

    # create or update affiliation
    alias = {'alias': form.cleaned_data.get('alias')}
    fields = {'chat': chat, 'user': request.user, 'defaults': alias}
    affiliation, created = Affiliation.objects.update_or_create(**fields)

    return JsonResponse(_affiliation_to_dict(affiliation), status=201)


@login_required(login_url='/')
def report(request):

    # abort if invalid request
    should_abort = _should_abort(request, 'POST')
    if should_abort:
        return should_abort

    form = ReportForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors})

    pk = Message.get_id_from_hash(form.cleaned_data.get('key'))
    message = get_object_or_404(Message, pk=pk)
    report = Report.objects.create(message=message, user=request.user)
    return JsonResponse({'report': report.pk}, status=201)


def logout(request):
    auth_logout(request)
    return redirect(resolve_url('home'))


def _should_abort_user(request, should_redirect):

    # authorize if user is staff
    if request.user.is_staff:
        return False

    # authorize if user is female and not blocked
    not_female = False
    blocked = False
    if hasattr(request.user, 'profile'):
        if request.user.profile.gender == Profile.FEMALE:
            if not request.user.profile.blocked:
                return False
            else:
                blocked = True
        else:
            not_female = True

    auth_logout(request)
    if should_redirect:
        if not_female:
            return redirect(resolve_url('female_only'))
        elif blocked:
            return redirect(resolve_url('blocked'))

    return HttpResponseForbidden()


def _should_abort(request, allowed_methods, **kwargs):

    ajax_only = kwargs.get('ajax_only', True)
    should_redirect = False if ajax_only else True

    # abort if user is not valid
    should_abort = _should_abort_user(request, should_redirect)
    if should_abort:
        return should_abort

    # only accept AJAX requests
    if not request.is_ajax() and kwargs.get('ajax_only', True):
        return HttpResponse(status=422)

    # only accept certain methods
    if isinstance(allowed_methods, str):
        allowed_methods = [allowed_methods]
    if request.method not in allowed_methods:
        return HttpResponseNotAllowed(allowed_methods)

    return None


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
            'key': message.hash_id,
            'className': css_class}


def _affiliations_to_ctx(user):
    output = list()
    for affiliation in Affiliation.objects.filter(user=user):
        output.append(_affiliation_to_dict(affiliation))
    return output


def _affiliation_to_dict(affiliation):
    return dict(url=resolve_url('app:chat', affiliation.chat.hash_id),
                key=affiliation.hash_id,
                alias=affiliation.alias,
                active=affiliation.active,
                valentinas=affiliation.chat.affiliation_set.count())
