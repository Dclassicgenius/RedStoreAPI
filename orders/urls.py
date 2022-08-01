from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('orders/<int:pk>/status/', views.UpdateOrderStatus.as_view(), name='order-status'),
   
]