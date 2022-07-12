from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductCreateListView.as_view(), name='product-list-create'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
   
]