"""
Contains custom models for the purchasing app.

Documentation for Django models found at 
https://docs.djangoproject.com/en/2.2/topics/db/models/

Documentation for customizing default Django User model found at
https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
"""

from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# custom manager for custom user model. Intended to be compatible with Django admin
class UserManager(BaseUserManager):
    """Customized manager for custom user class."""

    def create_user(self, email, first_name, last_name, password=None):
        """Creates a new user."""
        if not email:
            raise ValueError('Users must have an email address')

        new_user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        new_user.set_password(password)

        new_user.save()
        return new_user
    
    def create_superuser(self, email, first_name, last_name, password=None):
        """Creates a new user and sets is_superuser to True."""
        if not email:
            raise ValueError('Users must have an email address')

        new_user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        new_user.django_admin = True
        new_user.access_level = User.ADMINISTRATOR

        new_user.save()
        return new_user


# custom user model. Inteded to be compatible with Django admin
class User(AbstractBaseUser):
    """Customized user model using Django's authentication system."""

    # custom user model configurations required by Django
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    # for booleans in html select
    BOOLEANS_AS_INTS = (
        (True, 1),
        (False, 0)
    )

    # configure access level choices
    LICENCEE = 1
    PURCHASER = 2
    ADMINISTRATOR = 3
    ACCESS_LEVEL_CHOICES = [
        (LICENCEE, 'Licencee'),
        (PURCHASER, 'Purchaser'),
        (ADMINISTRATOR, 'Administrator')
    ]

    # access level default home pages when authenticated
    DEFAULT_HOME = {
        LICENCEE: 'logout',
        PURCHASER: 'shop',
        ADMINISTRATOR: 'products'
    }

    # attributes
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64)
    suffix_name = models.CharField(max_length=3, null=True, blank=True)
    address_1 = models.CharField(max_length=128, null=True, blank=True)
    address_2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    postal = models.CharField(max_length=16, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    access_level = models.IntegerField(default=PURCHASER, choices=ACCESS_LEVEL_CHOICES)

    # is_active is used by Django's authentication system
    is_active = models.BooleanField(default=True)
    # Since the Django admin permissions are not being used there is no need
    # to store both is_staff and is_superuser. We refer to this attribute in
    # properties to maintain compatibility with the Django admin.
    django_admin = models.BooleanField(default=False)

    group = models.ForeignKey(
        'Group',
        null=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )

    @property
    def is_staff(self):
        """Validates if user has permission to access the Django admin."""
        return self.django_admin
    
    @property
    def is_superuser(self):
        """User has all permissions in the Django admin."""
        return self.django_admin
    
    @property
    def default_home(self):
        """The reverse lookup view name for this user's default home page."""
        return self.DEFAULT_HOME[self.access_level]

    @property
    def access_level_name(self):
        """Returns access level by descriptive name."""
        for value, name in self.ACCESS_LEVEL_CHOICES:
            if self.access_level == value:
                return name
    
    @property
    def cart_size(self):
        """Returns the number of items in the user cart."""
        return 0

    # methods
    def __str__(self):
        """String method for class."""
        return self.email

    def __repr__(self):
        """Representation method for class."""
        return f'User(email={self.email})'
    
    # these two recomended by Djanjo documentation
    def get_full_name(self):
        """Returns user's full name."""
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        """Returns user's first name."""
        return self.first_name
    
    # these two required for Django admin compatibility
    def has_perm(self, perm, obj=None):
        """Checks if the user has a specific permission."""
        return True
    
    def has_module_perms(self, app_label):
        """Checks if the user has permission to view the app."""
        return True
    
    @classmethod
    def is_email_taken(cls, email):
        """Checks if a user with provided email already exists."""
        try:
            if cls.objects.get(email=cls.objects.normalize_email(email)):
                return True
        except cls.DoesNotExist:
            return False

    @staticmethod
    def compare_passwords(password, confirm_password):
        """Compares passwords and returns password if they match."""
        if password == confirm_password:
            return password
        else:
            raise RuntimeError('Passwords do not match')


# APP SPECIFIC MODELS
class Group(models.Model):
    """Class for grouping like users together."""
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        """String method for class."""
        return self.name
    
    def __repr__(self):
        """Representation method for class."""
        return f'Group(name={self.name})'


class Product(models.Model):
    """Class for storing product information."""
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    cost = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    @property
    def dollar_cost(self):
        """Returns the cost in dollars."""
        dollar_cost = round(Decimal((self.cost / 100)), 2)
        return f'${dollar_cost}'

    def __str__(self):
        """String method for class."""
        return self.name
    
    def __repr__(self):
        """Representation method for class."""
        return f'Product(name={self.name}, code={self.code})'


class Coupon(models.Model):
    """Stores data about coupons."""
    code = models.CharField(max_length=16, unique=True)
    discount = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    @property
    def discount_dollar_cost(self):
        """Returns the discount in dollars."""
        dollars = round(Decimal((self.discount / 100)), 2)
        return f'${dollars}'

    def __str__(self):
        """String method for class."""
        return self.code
    
    def __repr__(self):
        """Representation method for class."""
        return f'Coupon(id={self.code})'


class Transaction(models.Model):
    """Stores a user's transaction data."""

    # define type choices
    CREDIT = 1
    INVOICE = 2
    TYPE_CHOICES = [
        (CREDIT, 'Credit'),
        (INVOICE, 'Invoice')
    ]

    # define status choices
    UNPAID = 0
    PENDING = 1
    PAID = 2
    DECLINED = 3
    STATUS_CHOICES = [
        (UNPAID, 'Unpaid'),
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (DECLINED, 'Declined')
    ]
    
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    
    type = models.IntegerField(null=True, default=None, choices=TYPE_CHOICES)
    status = models.IntegerField(default=UNPAID, choices=STATUS_CHOICES)
    date = models.DateTimeField(null=True, blank=True)

    coupon = models.ForeignKey(
        'Coupon',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )

    @property
    def grand_total(self):
        """Returns the grand total for this transaction."""
        grand_total = 0
        for license in self.licenses.all():
            grand_total += license.price_at_purchase
        return grand_total

    def __str__(self):
        """String method for class."""
        return self.id
    
    def __repr__(self):
        """Representation method for class."""
        return f'Transaction(id={self.id}, user={self.user.id})'
    
    def set_pending(self):
        """Set the status to pending."""
        self.status = PENDING
        self.date = datetime.now()
        self.save()
    
    def set_paid(self):
        """Set the status to paid."""
        self.status = PAID
        self.date = datetime.now()
        self.save()
    
    def set_declined(self):
        """Set the status to declined."""
        self.status = DECLINED
        self.date = datetime.now()
        self.save()


class License(models.Model):
    """Stores licence data."""

    transaction = models.ForeignKey(
        'Transaction',
        on_delete=models.CASCADE,
        related_name='licenses'
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.DO_NOTHING,
        related_name='licenses'
    )

    user = models.ForeignKey(
        'User',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='licenses'
    )

    price_at_purchase = models.IntegerField(default=0)
    in_use = models.BooleanField(default=False)

    def __str__(self):
        """String method for class."""
        return self.id
    
    def __repr__(self):
        """Representation method for class."""
        return f'License(id={self.id})'