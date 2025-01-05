from django.db import models

# Create your models here.
from django.conf import settings  

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