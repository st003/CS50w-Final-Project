"""Purchasing app's views."""

from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render, reverse


# index
def index(request):
    return render(request, 'purchasing/index.html')


# login, logout, and registration views
def login_view(request):

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

 