from django.contrib.auth import get_user_model
from .models import (
    Student,
)

from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ValidationError,
    BooleanField,
)


class UserRegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = Student  
        fields = [
            'username', 'email' , 'college' , 'semester' , 'password'
        ]

    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        user = Student.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            college=validated_data['college'],
            semester=validated_data['semester'],
            default_payment_methods=validated_data.get('default_payment_methods', []),
        )
        return user


