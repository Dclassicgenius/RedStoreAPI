from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductCreateListView.as_view(), name='product-list-create'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('review/', views.ReviewRatingCreateListView.as_view(), name='review-list-create'),
    path('review/<int:pk>/', views.ReviewRatingDetailView.as_view(), name='review-detail'),
    path('product-gallery/', views.ProductGalleryListCreateView.as_view(), name='product-gallery-list-create'),
    path('product-gallery/<int:pk>/', views.ProductGalleryDetailView.as_view(), name='product-gallery-detail'),
   
   
]