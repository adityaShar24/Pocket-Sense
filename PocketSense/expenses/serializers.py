
from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    IntegerField,
    DecimalField,
    Serializer,
    EmailField
)
from rest_framework.serializers import ValidationError

from .models import (
    Category,
    Expense,
    ExpenseSplit,
)

from CoreAuth.models import (
    Student,
)

from .utils import (
    handle_expense_split,
)

class CategorieSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id' , 'name', 'is_custom']
        
class ExpenseSplitSerializer(Serializer):
    email = EmailField(required=True)
    amount = DecimalField(max_digits=10, decimal_places=2)
            
class ExpenseSerializer(ModelSerializer):
    splits = ExpenseSplitSerializer(many=True, write_only=True)

    class Meta:
        model = Expense
        fields = ['amount', 'category', 'split_type', 'receipt_image', 'splits', 'student', 'paid_by', 'paid_by_you']

    def create(self, validated_data):
        splits_data = validated_data.pop("splits")
        expense_amount = validated_data.get("amount")
        split_type = validated_data.get("split_type")
        email = validated_data.get('email')

        # Validate and calculate splits for safety
        try:
            validated_splits = handle_expense_split(expense_amount, split_type, splits_data)
        except ValidationError as e:
            raise ValidationError({"splits": str(e)})

        # Create the Expense object
        expense = Expense.objects.create(**validated_data)

        # Create the associated ExpenseSplit objects
        for split_data in validated_splits:
            email = split_data.get('email')
            amount = split_data.get('amount')
            ExpenseSplit.objects.create(expense=expense, email=email, amount=amount)

        return expense