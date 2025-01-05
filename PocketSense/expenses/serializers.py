
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
        
class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'split_type', 'student', 'receipt_image']
        
class ExpenseSplitSerializer(Serializer):
    student_id = IntegerField()
    amount = DecimalField(max_digits=10, decimal_places=2)
