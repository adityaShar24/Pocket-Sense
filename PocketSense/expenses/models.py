from django.db import models

# Create your models here.
from django.conf import settings  
from CoreAuth.models import (
    Student,
)
from .enums import (
    PaymentStatusEnum,
    PaymentMethodEnum,
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
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_groups")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="expense_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    
class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    split_type = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses", null=True , blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="created_expenses")
    paid_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="paid_expenses")
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_by_you = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.amount} - {self.category} - {self.student} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']


class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="splits")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField() 
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.email} owes {self.amount} for {self.expense}"
    
    
class Settlement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lent_settlements"
    )   
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowed_settlements"
    )
    payment_status = models.CharField(max_length=20, choices=PaymentStatusEnum.choices(), default=PaymentStatusEnum.Pending.value)
    settlement_method = models.CharField(max_length=20, choices=PaymentMethodEnum.choices())
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_status}"
