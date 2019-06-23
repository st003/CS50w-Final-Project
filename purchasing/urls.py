"""Purchasing app's urls."""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('coupon/', views.coupon, name='coupon'),
    path('coupon/<int:coupon_id>', views.coupon, name='coupon'),
    path('coupons/', views.coupons, name='coupons'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('manage_product/', views.manage_product, name='manage_product'),
    path('manage_product/<int:product_id>', views.manage_product, name='manage_product'),
    path('products/', views.products, name='products'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('purchase_product/<int:product_id>', views.purchase_product, name='purchase_product'),
    path('register/', views.register, name='register'),
    path('reports/', views.reports, name='reports'),
    path('shop/', views.shop, name='shop'),
    path('user/', views.user, name='user'),
    path('user/<int:user_id>', views.user, name='user'),
    path('user_license/', views.user_license, name='user_license'),
    path('users/', views.users, name='users')
]