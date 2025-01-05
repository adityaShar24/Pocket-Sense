
from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ValidationError,
    BooleanField,
)
from .models import (
    Category,
    Expense
)

from CoreAuth.models import (
    Student,
)

class CategorieSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id' , 'name', 'is_custom']
        
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'split_type', 'student', 'date', 'receipt_image']
        
class ExpenseSplitSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
