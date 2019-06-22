"""Purchasing app's urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('coupon/', views.coupon, name='coupon'),
    path('coupon/<int:coupon_id>', views.coupon, name='coupon'),
    path('coupons/', views.coupons, name='coupons'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product/', views.product, name='product'),
    path('product/<int:product_id>', views.product, name='product'),
    path('products/', views.products, name='products'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('register/', views.register, name='register'),
    path('reports/', views.reports, name='reports'),
    path('shop/', views.shop, name='shop'),
    path('user/', views.user, name='user'),
    path('user/<int:user_id>', views.user, name='user'),
    path('user_license/', views.user_license, name='user_license'),
    path('users/', views.users, name='users')
]