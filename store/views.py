from django.shortcuts import get_object_or_404
from rest_framework import generics, status, mixins
from .permissions import IsOwnerOfObject

from .models import Product, ReviewRating, ProductGallery
from .serializers import ProductCreationListSerializer, ProductDetailSerializer, ProductGallerySerializer, ReviewRatingSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

class ProductCreateListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreationListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(operation_summary="Create a product")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class ProductDetailView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(operation_summary="Get a product")
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update a product")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Delete a product")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewRatingCreateListView( mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get review ratings")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary="Create a review rating")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReviewRatingDetailView(generics.GenericAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
    permission_classes = [IsOwnerOfObject]


    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
    
    @swagger_auto_schema(operation_summary="Get a review rating")
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Update a review rating")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Delete a review rating")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductGalleryListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ProductGallery.objects.all()
    serializer_class = ProductGallerySerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get product gallery")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary="Create a product gallery")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductGalleryDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = ProductGallery.objects.all()
    serializer_class = ProductGallerySerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get a product gallery")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  

    @swagger_auto_schema(operation_summary="Update a product gallery")
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary="Delete a product gallery")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)





