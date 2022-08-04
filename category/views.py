from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class CategoryCreateListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Create product category")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()


class CategoryDetailView(generics.GenericAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(operation_summary="Get category details")
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Update caetegory details")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Delete category")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    


   