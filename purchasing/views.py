"""Purchasing app's views."""

from django.shortcuts import render


# index
def index(request):
    return render(request, 'purchasing/index.html')
