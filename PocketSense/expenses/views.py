from datetime import datetime , timedelta
from django.shortcuts import render
from django.db.models import Count, Sum , F, Value
from django.db.models.functions import Coalesce
from decimal import Decimal

from rest_framework.permissions import IsAuthenticated , BasePermission
from rest_framework.serializers import ValidationError

from rest_framework.views import (
    APIView,
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)

from .models import (
    Category,
    Expense,
    Group,
    Settlement,
    Budget,
)

from .serializers import (
    CategorieSerializer,
    ExpenseSerializer,
    GroupSerializer,
    SettlementSerializer,
    CategorizedExpenseSerializer,
    BudgetSerializer,
    MonthlyBudgetTrackingSerializer,
) 

from utils.response import (
    response_200,
    response_400_bad_request,
)
from .utils import (
    handle_expense_split,
)

from .enums import (
    PaymentStatusEnum,
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
        
        student = request.user
        category = data.get('category')
        
        try:
            budget = Budget.objects.get(student=student, category=category)
        except Budget.DoesNotExist:
            raise ValidationError(f"No budget found for student {student} in category {category}")

        remaining_budget = budget.budget_limit - expense_amount
        if remaining_budget < 0:
            raise ValidationError("Expense exceeds the budget limit.")

        budget.budget_limit = remaining_budget
        budget.save()
        logger.info(f"Serializer Data: {serializer.validated_data}")

        self.perform_create(serializer)

        return response_200("Expense Created", serializer.data)


class GroupListCreateRetrieveUpdateDestroyView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = 'pk'
    
    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        group.members.add(self.request.user)

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)     
        return response_200("Group created successfully", response.data)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        response = super().update(request , *args , **kwargs)
        return response_200("Group Updated Successfully", response.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        response = super().destroy(request, *args, **kwargs)
        return response_200("Group deleted successfully", response.data)

class SettlementListCreateRetrieveUpdateDestroyView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SettlementSerializer
    queryset = Settlement.objects.all()
    lookup_field = 'pk'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)     
        return response_200("Settlement created successfully", response.data)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            queryset = self.get_queryset()
            
            overdue_settlements = queryset.filter(due_date__lt=datetime.now(), payment_status=PaymentStatusEnum.Pending.value)
            
            upcoming_due_date = datetime.now() + timedelta(days=7)
            
            due_soon_settlements = queryset.filter(
                due_date__range=[datetime.now(), upcoming_due_date],
                payment_status=PaymentStatusEnum.Pending.value
            )
            
            overdue_serializer = self.get_serializer(overdue_settlements, many=True)
            due_soon_serializer = self.get_serializer(due_soon_settlements, many=True)
            all_settlements_serializer = self.get_serializer(queryset, many=True)
            return response_200(
                {
                    "all_settlements": all_settlements_serializer.data,
                    "overdue_settlements": overdue_serializer.data,
                    "due_soon_settlements": due_soon_serializer.data
                }
            )

    def put(self, request, *args, **kwargs):
        response = super().update(request , *args , **kwargs)
        return response_200("Settlement Updated Successfully", response.data)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request , *args , **kwargs)
        return response_200("Settlement deleted successfully")

#analysis

class MonthlyAnalysisView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        month = int(request.query_params.get('month', datetime.now().month))
        year = int(request.query_params.get('year', datetime.now().year))

        settlements = Settlement.objects.filter(
            user=request.user,
            created_at__year=year,
            created_at__month=month,
        )

        total_settlements = settlements.count()
        total_pending = settlements.filter(payment_status=PaymentStatusEnum.Pending.value).count()
        total_completed = settlements.filter(payment_status=PaymentStatusEnum.Completed.value).count()

        total_amount_due = settlements.filter(payment_status=PaymentStatusEnum.Pending.value).aggregate(
            total=Sum('amount')
        )['total'] or 0

        settlement_method_breakdown = settlements.values('settlement_method').annotate(
            count=Count('id')
        ).order_by('-count')

        payment_status_breakdown = settlements.values('payment_status').annotate(
            count=Count('id')
        ).order_by('-count')

        data = {
            "month": month,
            "year": year,
            "summary": {
                "total_settlements": total_settlements,
                "total_pending": total_pending,
                "total_completed": total_completed,
                "total_amount_due": total_amount_due,
            },
            "breakdowns": {
                "settlement_method_breakdown": list(settlement_method_breakdown),
                "payment_status_breakdown": list(payment_status_breakdown),
            },
        }

        return response_200("Monthly Analysis",  data)
    
class GetExpenseCategorizationView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request , *args, **kwargs):
        logger.info(f"Request User:{request.user.email}")
        categorized_expenses = Expense.objects.filter(student=request.user).values('category__name').annotate(total=Sum('amount'))
        
        serializer = CategorizedExpenseSerializer(categorized_expenses, many=True)
        
        return response_200("Expense Categorization", serializer.data )

class BudgetListCreateRetrieveUpdateDestroyView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        return super().get_queryset().filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response_200("Budget created successfully", response.data)
        except Exception as e:
            return response_400_bad_request(f"Error while creating budget: {str(e)}")

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return response_200("Budget updated successfully", response.data)
        except Exception as e:
            return response_400_bad_request(f"Error while updating budget: {str(e)}")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        try:
            response = super().destroy(request, *args, **kwargs)
            return response_200("Budget deleted successfully", None)
        except Exception as e:
            return response_400_bad_request(f"Error while deleting budget: {str(e)}")
        
class BudgetAnalysisView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        logger.info(f"Request User: {request.user.email}")

        budgets = (
            Budget.objects.filter(student=request.user)
            .annotate(
                total_expenses=Coalesce(
                    Sum('category__expense__amount', filter=F('category__expense__student') == request.user),
                    Value(Decimal("0.00"))
                ),
                remaining_budget=F('budget_limit') - Coalesce(
                    Sum('category__expense__amount', filter=F('category__expense__student') == request.user),
                    Value(Decimal("0.00"))
                ),
            )
            .values('category__name', 'budget_limit', 'total_expenses', 'remaining_budget')
        )

        if not budgets:
            return response_400_bad_request("No budgets found for the user.")

        serializer = MonthlyBudgetTrackingSerializer(budgets, many=True)

        return response_200("Budget Analysis",serializer.data)
