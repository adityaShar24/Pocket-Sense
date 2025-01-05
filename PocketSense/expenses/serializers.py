from .models import Category

from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ValidationError,
    BooleanField,
)

class CategorieSerializer(ModelSerializer):
    class Meta:
        model = Category
        
    fields = "__all__"