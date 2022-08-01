from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('cart_items/', views.CartItemListCreateView.as_view(), name='cart-item-list-create'),
]