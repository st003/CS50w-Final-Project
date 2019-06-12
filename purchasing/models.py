"""
Contains custom models for the purchasing app.

Documentation for Django models found at

Documentation for customizing default Django User model found at
https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
"""

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

    # configure access level choices
    LICENCEE = 1
    PURCHASER = 2
    ADMINISTRATOR = 3
    ACCESS_LEVEL_CHOICES = [
        (LICENCEE, 'Licencee'),
        (PURCHASER, 'Purchaser'),
        (ADMINISTRATOR, 'Administrator')
    ]

    # class attributes
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
        """Valiidates if user has permission to access the Django admin."""
        return self.django_admin
    
    @property
    def is_superuser(self):
        """User has all permissions in the Django admin."""
        return self.django_admin

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

    def __str__(self):
        """String method for class."""
        return self.name
    
    def __repr__(self):
        """Representation method for class."""
        return f'Product(name={self.name}, code={self.code})'