from . import views
from django.urls import path


urlpatterns = [
    path('products/', views.ProductView().as_view(), name='product-view'),
    path('single-product/<int:product_id>/', views.ProductEditView().as_view(), name='single-product-view'),
    path('cart/', views.CartView().as_view(), name='cart-view'),
    path('cart-product-delete/<int:cart_id>/', views.CartEditView().as_view(), name='user-cart-edit'),
    path('pending-products/<int:cart_id>/', views.make_pending, name='pending-products'),
    path('deliver-products/<int:cart_id>/', views.delivered_products, name='delivered-products'),
]
