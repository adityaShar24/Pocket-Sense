from django.shortcuts import render
from decimal import Decimal

from rest_framework.permissions import IsAuthenticated , BasePermission
from rest_framework.serializers import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)

from .models import (
    Category,
    Expense
)

from .serializers import (
    CategorieSerializer,
    ExpenseSerializer
) 

from utils.response import (
    response_200,
    response_400_bad_request,
)
from .utils import (
    handle_expense_split,
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

class ExpenseCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['student'] = request.user.id

        paid_by_you = data.get('paid_by_you')
        if paid_by_you:
            data['paid_by'] = request.user.id
        else:
            paid_by = data.get('paid_by')
            if not paid_by:
                raise ValidationError("Need to add the payee")
            data['paid_by'] = paid_by

        # Parse splits data
        splits_data = data.get('splits', [])
        if not isinstance(splits_data, list):
            splits_data = []

        # Add the request user as a participant if split_type is equal
        split_type = data.get('split_type')
        expense_amount = Decimal(data.get('amount', '0'))

        if split_type == 'equal':
            # Add request user to splits
            request_user_email = request.user.email
            if not any(participant.get('email') == request_user_email for participant in splits_data):
                splits_data.append({'email': request_user_email})

            if not splits_data:
                raise ValidationError("Participants are required for an equal split.")

            num_participants = len(splits_data)
            if num_participants == 0:
                raise ValidationError("No participants provided for the equal split.")

        logger.info(f"Participants : {splits_data}")

        calculated_splits = handle_expense_split(expense_amount, split_type, splits_data)

        data['splits'] = calculated_splits

        # Serialize and validate data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        logger.info(f"Serializer Data: {serializer.validated_data}")

        self.perform_create(serializer)

        return response_200("Expense Created", serializer.data)


