"""saas_cart URL Configuration."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('purchasing.urls')),
    path('admin/', admin.site.urls)
]
