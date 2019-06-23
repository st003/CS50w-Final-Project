"""Purchasing app's views."""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Coupon, Group, Product, User, Transaction


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
            
            # check if user already exists
            if User.is_email_taken(request.POST['email']):
                raise RuntimeError('Email is already taken')
            
            # create the user
            User.objects.create_user(
                email=request.POST['email'],
                password=User.compare_passwords(
                    request.POST['password'],
                    request.POST['confirmPassword']
                ),
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
    """Displays available products for sale."""
    products = Product.objects.filter(active=True).all()
    return render(request, 'purchasing/shop.html', {'products': products})


@login_required
def purchase_product(request, product_id):
    """Displays the product page."""
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'purchasing/purchase_product.html', {'product': product})


@login_required
def cart(request, user_id):
    """Displays the user's shopping cart."""
    return render(request, 'purchasing/cart.html')


@login_required
def user_license(request):
    return render(request, 'purchasing/user_license.html')


@login_required
def purchase_history(request):
    return render(request, 'purchasing/purchase_history.html')


# ADMINISTRATOR views
@login_required
def products(request):
    """Displays the products page."""
    products = Product.objects.all()
    return render(request, 'purchasing/products.html', {'products': products})


@login_required
def manage_product(request, product_id=None):
    """Adds or Edits a product."""

    if request.method == 'GET':

        # existing product
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            return render(request, 'purchasing/manage_product.html', {'product': product})
        # new product
        else:
            return render(request, 'purchasing/manage_product.html')
    
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
                return redirect(reverse('manage_product', kwargs={'product_id': existing_product.pk}))
            
            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('manage_product', kwargs={'product_id': request.POST['id']}))
            
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

                messages.success(request, 'Product Created Successfully')
                return redirect(reverse('manage_product', kwargs={'product_id': new_product.pk}))
            
            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('manage_product'))


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

                messages.success(request, 'Coupon Created Successfully')
                return redirect(reverse('coupon', kwargs={'coupon_id': new_coupon.pk}))
                
            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('coupon'))
        

@login_required
def users(request):
    """Displays a list of users."""
    users = User.objects.all()
    return render(request, 'purchasing/users.html', {'users': users})


@login_required
def user(request, user_id=None):
    """Add or edit a user."""

    if request.method == 'GET':

        # existing user
        if user_id:
            context = {
                'existing_user': get_object_or_404(User, pk=user_id),
                'groups': Group.objects.all()
            }
            return render(request, 'purchasing/user.html', context)
        # new user
        else:
            groups = Group.objects.all()
            return render(request, 'purchasing/user.html', {'groups': groups})
    
    elif request.method == 'POST':

        # existing user
        if request.POST.get('id'):

            try:

                # required field validation
                if not request.POST.get('email'):
                    raise RuntimeError('email not provided')
                if not request.POST.get('firstName'):
                    raise RuntimeError('First name not provided')
                if not request.POST.get('lastName'):
                    raise RuntimeError('Last name not provided')
                
                existing_user = User.objects.get(pk=request.POST['id'])

                # login info
                existing_user.email = request.POST['email']

                # update password if present
                if request.POST.get('password') or request.POST.get('confirmPassword'):
                    existing_user.email = User.compare_passwords(
                        request.POST.get('password'),
                        request.POST.get('confirmPassword')
                    )

                # name info
                existing_user.first_name = request.POST['firstName']
                existing_user.last_name = request.POST['lastName']
                existing_user.middle_name = request.POST['middleName']
                existing_user.suffix_name = request.POST['suffixName']

                # address info
                existing_user.address_1 = request.POST['address1']
                existing_user.address_2 = request.POST['address2']
                existing_user.city = request.POST['city']
                existing_user.state = request.POST['state']
                existing_user.postal = request.POST['postal']
                existing_user.country = request.POST['country']

                # settings
                existing_user.access_level = request.POST['accessLevel']
                existing_user.is_active = int(request.POST['isActive']) # converted to int b/c boolean
                existing_user.group = Group.objects.get(pk=request.POST['group'])

                existing_user.save()
                messages.success(request, 'Changes Saved')
                return redirect(reverse('user', kwargs={'user_id': existing_user.pk}))

            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('user', kwargs={'user_id': request.POST['id']}))
        
        # new user
        else:

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

                # check if user already exists
                if User.is_email_taken(request.POST['email']):
                    raise RuntimeError('Email is already taken')

                new_user = User.objects.create_user(
                    email=request.POST['email'],
                    password=User.compare_passwords(
                        request.POST['password'],
                        request.POST['confirmPassword']
                    ),
                    first_name = request.POST['firstName'],
                    last_name = request.POST['lastName']
                )

                # name info
                new_user.middle_name = request.POST['middleName']
                new_user.suffix_name = request.POST['suffixName']

                # address info
                new_user.address_1 = request.POST['address1']
                new_user.address_2 = request.POST['address2']
                new_user.city = request.POST['city']
                new_user.state = request.POST['state']
                new_user.postal = request.POST['postal']
                new_user.country = request.POST['country']

                # settings
                new_user.access_level = request.POST['accessLevel']
                new_user.is_active = int(request.POST['isActive']) # converted to int b/c boolean
                new_user.group = Group.objects.get(pk=request.POST['group'])

                new_user.save()
                messages.success(request, 'User Created Successfully')
                return redirect(reverse('user', kwargs={'user_id': new_user.pk}))

            except Exception as error:
                messages.error(request, error)
                return redirect(reverse('user'))


@login_required
def reports(request):
    """Renders the reports page."""
    transactions = Transaction.objects.all()
    return render(request, 'purchasing/reports.html', {'transactions': transactions})