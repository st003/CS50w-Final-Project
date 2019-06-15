"""Purchasing app's views."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, reverse


# index
def index(request):
    """Index view. There's nothing here."""
    return render(request, 'purchasing/index.html')


# login, logout, and registration views
def login_view(request):
    """Renders the login page an authenticates login attempts."""

    if request.method == 'GET':

        if request.user.is_authenticated:
            return redirect(reverse('shop'))
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
            return redirect(reverse('shop'))
        else:
            return redirect(reverse('login'))


def logout_view(request):
    """Logs out the current user."""
    logout(request)
    return redirect(reverse('login'))


# AUTHENTICATED VIEWS

# purchaser views
@login_required
def shop(request):
    return render(request, 'purchasing/shop.html')


@login_required
def user_license(request):
    return render(request, 'purchasing/user_license.html')


@login_required
def purchase_history(request):
    return render(request, 'purchasing/purchase_history.html')


@login_required
def account_settings(request):
    return render(request, 'purchasing/account_settings.html')