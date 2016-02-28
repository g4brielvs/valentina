from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, resolve_url
from valentina.app.models import Profile


@login_required(login_url='/')
def welcome(request):

    # abort if request has no user
    if not request.user:
        return redirect(resolve_url('home'))

    # abort if user is not valid
    if not _valid_user(request.user):
        return redirect(resolve_url('female_only'))

    return render(request, 'app/home.html')


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
