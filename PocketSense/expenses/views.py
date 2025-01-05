from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
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
)

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a category to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        return obj.user == request.user


class CategoryListCreateRetrieveUpdateDestroyView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # Apply custom permissions here
    serializer_class = CategorieSerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        # Limit the queryset to the categories created by the logged-in user
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response_200("Category added successfully", response.data)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Ensure the user has permission to update
        instance = self.get_object()
        if not self.check_permissions(request, instance):
            raise PermissionDenied("You do not have permission to update this category.")
        response = super().update(request, *args, **kwargs)
        return response_200("Category updated successfully", response.data)

    def delete(self, request, *args, **kwargs):
        # Ensure the user has permission to delete
        instance = self.get_object()
        if not self.check_permissions(request, instance):
            raise PermissionDenied("You do not have permission to delete this category.")
        response = super().destroy(request, *args, **kwargs)
        return response_200("Category deleted successfully", response.data)
