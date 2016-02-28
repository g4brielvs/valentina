from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render, resolve_url


def home(request):
    if request.user.is_authenticated():
        return redirect(resolve_url('app:welcome'))
    return render(request, 'home.html')


def logout(request):
    auth_logout(request)
    return redirect(resolve_url('home'))
