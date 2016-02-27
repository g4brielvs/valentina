from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, resolve_url


def home(request):
    if request.user.is_authenticated():
        return redirect(resolve_url('app'))
    return render(request, 'home.html')


@login_required(login_url='/')
def app(request):
    return HttpResponse()


def logout(request):
    auth_logout(request)
    return redirect(resolve_url('home'))
