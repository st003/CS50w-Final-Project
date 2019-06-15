"""Purchasing app's urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('shop/', views.shop, name='shop'),
    path('user_license/', views.user_license, name='user_license')
]