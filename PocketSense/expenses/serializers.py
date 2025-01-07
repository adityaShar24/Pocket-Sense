
from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    IntegerField,
    DecimalField,
    Serializer,
    EmailField,
    ListField,
    
)
from rest_framework.serializers import ValidationError

from .models import (
    Category,
    Expense,
    ExpenseSplit,
    Group
)

from CoreAuth.models import (
    Student,
)

from CoreAuth.serializers import (
    StudentSerializer,
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

class GroupSerializer(ModelSerializer):
    """Serializer for the Group model."""
    members = StudentSerializer(many=True, read_only=True)  # Nested serializer for students
    member_ids = ListField(
        child= IntegerField(), write_only=True, required=False,
        help_text="List of student IDs to add/remove as group members."
    )

    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'members', 'member_ids')
        
    def validate(self, data):
        member_ids = data.get('member_ids', [])
        if len(member_ids) < 2:
            raise ValidationError({"member_ids": "A group must have at least two members."})
        return data

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        group = Group.objects.create(**validated_data)
        if member_ids:
            group.members.set(Student.objects.filter(id__in=member_ids))
        return group

    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if member_ids is not None:
            instance.members.set(Student.objects.filter(id__in=member_ids))
        return instance