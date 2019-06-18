"""Purchasing app's views."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, reverse

from .models import Product, User

# PUBLIC VIEWS

def index(request):
    """Index view. There's nothing here."""
    return render(request, 'purchasing/index.html')


# login, logout, and registration views
def login_view(request):
    """Renders the login page an authenticates login attempts."""

    if request.method == 'GET':

        if request.user.is_authenticated:
            return redirect(reverse(request.user.default_home))
        else:
            return render(request, 'purchasing/login.html')
    
    elif request.method == 'POST':

        # required field validation
        if not request.POST.get('email'):
            raise Http404('Email not provided')
        if not request.POST.get('password'):
            raise Http404('Password not provided')

        user = authenticate(
            request,
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect(reverse(user.default_home))
        else:
            return redirect(reverse('login'))


def logout_view(request):
    """Logs out the current user."""
    logout(request)
    return redirect(reverse('login'))


def register(request):
    """Loads the registration page and creates new users."""
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            return redirect(reverse(request.user.default_home))
        else:
            return render(request, 'purchasing/register.html')
    
    elif request.method == 'POST':

        # required field validation
        if not request.POST.get('email'):
            raise Http404('Email not provided')
        if not request.POST.get('password'):
            raise Http404('Password not provided')
        if not request.POST.get('confirmPassword'):
            raise Http404('Confirm Password not provided')
        if not request.POST.get('firstName'):
            raise Http404('First Name not provided')
        if not request.POST.get('lastName'):
            raise Http404('Last Name not provided')
        
        # compare password inputs
        if request.POST.get('password') != request.POST.get('confirmPassword'):
            raise Http404('Passwords do not match')
        
        # check if user already exists
        if User.is_email_taken(request.POST.get('email')):
            raise Http404('Email is already taken')
        
        # create the user
        User.objects.create_user(
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            first_name=request.POST.get('firstName'),
            last_name=request.POST.get('lastName'),
        )

        # Authenticate and login the new user
        user = authenticate(
            request,
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect(reverse(user.default_home))
        else:
            return redirect(reverse('register'))


# AUTHENTICATED VIEWS

# PURCHASER views
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


# ADMINISTRATOR views
@login_required
def products(request):
    """Displays the products page."""
    products = Product.objects.all()
    return render(request, 'purchasing/products.html', {'products': products})


@login_required
def coupons(request):
    return render(request, 'purchasing/coupons.html')


@login_required
def user_group(request):
    return render(request, 'purchasing/user_group.html')


@login_required
def reports(request):
    return render(request, 'purchasing/reports.html')