from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserListCreateView.as_view(), name='user-list'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    # path('user/<int:pk>/profile/', views.UserProfileListCreateView.as_view(), name='user-profile'),


]