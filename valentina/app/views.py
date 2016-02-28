from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, resolve_url
from valentina.app.models import Profile
# from django.shortcuts import render


@login_required(login_url='/')
def welcome(request):

    # abort if request has no user
    if not request.user:
        return redirect(resolve_url('home'))

    # abort if user is not valid
    if not _valid_user(request.user):
        return redirect(resolve_url('app:female_only'))

    return HttpResponse()


def female_only(request):
    return HttpResponse()


def blocked(request):
    return HttpResponse()


def _valid_user(user):

    # authorize if user is staff
    if user.is_staff:
        return True

    # authorize if user is female
    if hasattr(user, 'profile'):
        if user.profile.gender == Profile.FEMALE:
            return True

    return False
