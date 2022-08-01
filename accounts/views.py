from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Account
from .permissions import IsOwnerOfObject
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import  AccountCreationSerializer, AccountDetailSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class UserListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreationSerializer
    permission_classes = []
    
    @swagger_auto_schema(operation_summary="Create a user account")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def perform_create(self, serializer):

        serializer.save()
    
class UserDetailView(generics.GenericAPIView):

    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer
    permission_classes = [IsAdminUser, IsOwnerOfObject, IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))

    @swagger_auto_schema(operation_summary="Get a user account")    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Update a user account")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(operation_summary="Delete a user account")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
