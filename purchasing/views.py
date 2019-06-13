"""Purchasing app's views."""

from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import redirect, render, reverse


# index
def index(request):
    """Index view. There's nothing here."""
    return redirect(reverse('shop'))


# login, logout, and registration views
def login_view(request):
    """Renders the login page an authenticates login attempts."""

    if request.method == 'GET':

        if request.user.is_authenticated:
            return redirect(reverse('index'))
        else:
            return render(request, 'purchasing/login.html')
    
    elif request.method == 'POST':

        # required field validation
        if not request.POST.get('email'):
            raise Http404('No email provided')
        if not request.POST.get('password'):
            raise Http404('No password provided')

        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password']
        )

        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            return redirect(reverse('login'))


def logout_view(request):
    """Logs out the current user."""
    logout(request)
    return redirect(reverse('login'))


# shop views
def shop(request):
    return render(request, 'purchasing/shop.html')