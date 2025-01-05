from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated , BasePermission
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import (
    Category,
)

from .serializers import (
    CategorieSerializer,
) 

from utils.response import (
    response_200,
    response_400_bad_request,
)

import logging

logger = logging.getLogger(__name__)

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a category to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.created_by == request.user


class CategoryListCreateRetrieveUpdateDestroyView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # Apply custom permissions here
    serializer_class = CategorieSerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['is_custom'] = True
        serializer = self.serializer_class(
            data=data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            category = serializer.save(created_by=request.user)
            return response_200("Category added successfully", serializer.data)
        logger.info(f"Category creation failed: {serializer.errors}")
        return response_400_bad_request(f"Category creation failed:{serializer.errors}")

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)

        data = request.data.copy()
        data['is_custom'] = True
        serializer = self.serializer_class(
            instance, data=data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            category = serializer.save(updated_by=request.user)
            return response_200("Category updated successfully", serializer.data)
        
        logger.info(f"Category update failed: {serializer.errors}")
        return response_400_bad_request(f"Category update failed: {serializer.errors}")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        response = super().destroy(request, *args, **kwargs)
        return response_200("Category deleted successfully", response.data)
