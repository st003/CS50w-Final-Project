"""Purchasing app's views."""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Coupon, Product, User


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

        try:

            # required field validation
            if not request.POST.get('email'):
                raise RuntimeError('Email not provided')
            if not request.POST.get('password'):
                raise RuntimeError('Password not provided')

            user = authenticate(
                request,
                username=request.POST['email'],
                password=request.POST['password']
            )

            if user is not None:
                login(request, user)
                return redirect(reverse(user.default_home))
            else:
                return redirect(reverse('login'))
        
        except Exception as error:
            messages.error(request, error)
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

        try:

            # required field validation
            if not request.POST.get('email'):
                raise RuntimeError('Email not provided')
            if not request.POST.get('password'):
                raise RuntimeError('Password not provided')
            if not request.POST.get('confirmPassword'):
                raise RuntimeError('Confirm Password not provided')
            if not request.POST.get('firstName'):
                raise RuntimeError('First Name not provided')
            if not request.POST.get('lastName'):
                raise RuntimeError('Last Name not provided')
            
            # compare password inputs
            if request.POST['password'] != request.POST['confirmPassword']:
                raise RuntimeError('Passwords do not match')
            
            # check if user already exists
            if User.is_email_taken(request.POST['email']):
                raise RuntimeError('Email is already taken')
            
            # create the user
            User.objects.create_user(
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['firstName'],
                last_name=request.POST['lastName'],
            )

            # Authenticate and login the new user
            user = authenticate(
                request,
                username=request.POST['email'],
                password=request.POST['password']
            )

            if user is not None:
                login(request, user)
                return redirect(reverse(user.default_home))
            else:
                return redirect(reverse('register'))
        
        except Exception as error:
            messages.error(request, error)
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
def product(request, product_id=None):
    """Adds or Edits a product."""

    if request.method == 'GET':

        # existing product
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            return render(request, 'purchasing/product.html', {'product': product})
        # new product
        else:
            return render(request, 'purchasing/product.html')
    
    elif request.method == 'POST':

        # existing product
        if request.POST.get('id'):

            try:
            
                # required field validation
                if not request.POST.get('name'):
                    raise RuntimeError('Name not provided')
                if not request.POST.get('code'):
                    raise RuntimeError('Code not provided')
                if not request.POST.get('cost'):
                    raise RuntimeError('Cost not provided')
                
                existing_product = Product.objects.get(pk=request.POST['id'])
                existing_product.code = request.POST['code']
                existing_product.name = request.POST['name']
                existing_product.cost = int(request.POST['cost'])
                existing_product.save()

                messages.success(request, 'Changes Saved')
                return redirect(reverse('product', kwargs={'product_id': existing_product.pk}))
            
            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('product', kwargs={'product_id': request.POST['id']}))
            
        # new product
        else:

            try:
            
                # required field validation
                if not request.POST.get('name'):
                    raise RuntimeError('Name not provided')
                if not request.POST.get('code'):
                    raise RuntimeError('Code not provided')
                if not request.POST.get('cost'):
                    raise RuntimeError('Cost not provided')
                
                new_product = Product(
                    code=request.POST['code'],
                    name=request.POST['name'],
                    cost=int(request.POST['cost'])
                )

                new_product.save()

                messages.success(request, 'Product Created')
                return redirect(reverse('product', kwargs={'product_id': new_product.pk}))
            
            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('product'))


@login_required
def coupons(request):
    """Displays the products page."""
    coupons = Coupon.objects.all()
    return render(request, 'purchasing/coupons.html', {'coupons': coupons})


@login_required
def coupon(request, coupon_id=None):
    """Adds or edits a coupon."""

    if request.method == 'GET':
        
        # existing coupon
        if coupon_id:
            coupon = get_object_or_404(Coupon, pk=coupon_id)
            return render(request, 'purchasing/coupon.html', {'coupon': coupon})
        # new coupon
        else:
            return render(request, 'purchasing/coupon.html')
    
    elif request.method == 'POST':
        
        # existing coupon
        if request.POST.get('id'):

            try:

                # required field validation
                if not request.POST.get('code'):
                    raise RuntimeError('Code not provided')
                if not request.POST.get('discount'):
                    raise RuntimeError('Discount not provided')
                
                existing_coupon = Coupon.objects.get(pk=request.POST['id'])
                existing_coupon.code = request.POST['code']
                existing_coupon.discount = int(request.POST['discount'])
                existing_coupon.save()

                messages.success(request, 'Changes Saved')
                return redirect(reverse('coupon', kwargs={'coupon_id': existing_coupon.pk}))
                
            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('coupon', kwargs={'coupon_id': request.POST['id']}))
        
        # new coupon
        else:

            try:

                # required field validation
                if not request.POST.get('code'):
                    raise RuntimeError('Code not provided')
                if not request.POST.get('discount'):
                    raise RuntimeError('Discount not provided')
                
                new_coupon = Coupon(
                    code=request.POST['code'],
                    discount=int(request.POST['discount'])
                )

                new_coupon.save()

                messages.success(request, 'Coupon Created')
                return redirect(reverse('coupon', kwargs={'coupon_id': new_coupon.pk}))
                
            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('coupon'))
        

@login_required
def user_group(request):
    return render(request, 'purchasing/user_group.html')


@login_required
def reports(request):
    return render(request, 'purchasing/reports.html')