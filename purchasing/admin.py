"""
Purchasing app's configuration for for the Django admin.

Documentation for customizing the default User model forms at
https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
"""

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group as auth_group

from .models import Group, License, Product, User, Transaction


# custom forms for the Django admin due to the customized user model
class UserCreationForm(forms.ModelForm):
    """Form for creating new users."""
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form for updating users."""
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'middle_name',
            'last_name',
            'suffix_name',
            'address_1',
            'address_2',
            'city',
            'state',
            'postal',
            'country',
            'access_level',
            'is_active',
            'django_admin',
        )

    def clean_password(self):
        return self.initial["password"]


# Override the default UserAdmin
class UserAdmin(BaseUserAdmin):
    """Defines the layout of the User model views in the Djano admin."""

    # forms
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'access_level')
    list_filter = ('access_level',)

    fieldsets = (
        ('Login Info', {'fields': ('email', 'password')}),
        ('Name Info', {'fields': ('first_name', 'middle_name', 'last_name', 'suffix_name')}),
        ('Address Info', {'fields': ('address_1', 'address_2', 'city', 'state', 'postal', 'country')}),
        ('Group', {'fields': ('group',)}),
        ('Permission Info', {'fields': ('access_level', 'is_active', 'django_admin')})
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# register models to the admin
admin.site.register(Group)
admin.site.register(License)
admin.site.register(Product)
admin.site.register(User, UserAdmin)
admin.site.register(Transaction)

# remove default models from the admin
admin.site.unregister(auth_group)
