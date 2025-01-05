from django.db import models

# Create your models here.
from django.conf import settings  
from CoreAuth.models import (
    Student,
)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "Food", "Travel"
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="categories"
    )
    is_custom = models.BooleanField(default=False)  # True if a user creates the category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    split_type = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.amount} - {self.category} - {self.student} - {self.date}"

    class Meta:
        ordering = ['-date']
