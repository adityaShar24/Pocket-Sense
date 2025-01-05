
from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    IntegerField,
    DecimalField,
    Serializer
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

class CategorieSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id' , 'name', 'is_custom']
        
class ExpenseSplitSerializer(Serializer):
    class Meta:
        model = ExpenseSplit
        fields = '__all__'
        
class ExpenseSerializer(ModelSerializer):
    splits = ExpenseSplitSerializer(many=True, write_only=True)

    class Meta:
        model = Expense
        fields = ['amount', 'category', 'split_type', 'receipt_image', 'splits', 'student', 'paid_by', 'paid_by_you']

    def create(self, validated_data):
        splits_data = validated_data.pop("splits")
        expense = Expense.objects.create(**validated_data)

        for split_data in splits_data:
            if 'amount' not in split_data:
                raise ValidationError("Each split must have a valid amount.")
            ExpenseSplit.objects.create(expense=expense, **split_data)

        return expense
