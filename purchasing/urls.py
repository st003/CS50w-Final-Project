"""Purchasing app's urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('coupons/', views.coupons, name='coupons'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.products, name='products'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('reports/', views.reports, name='reports'),
    path('shop/', views.shop, name='shop'),
    path('user_license/', views.user_license, name='user_license'),
    path('user_group/', views.user_group, name='user_group')
]