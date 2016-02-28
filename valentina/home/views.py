from django.contrib.auth import logout
from django.shortcuts import redirect, render, resolve_url


def home(request):
    if request.user.is_authenticated():
        return redirect(resolve_url('app:welcome'))
    return render(request, 'home/home.html')


def blocked(request):
    logout(request)
    return render(request, 'home/blocked.html')


def female_only(request):
    logout(request)
    return render(request, 'home/female_only.html')
