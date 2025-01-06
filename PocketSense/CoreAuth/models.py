import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class Student(AbstractUser):
    college = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    default_payment_methods = models.JSONField(default=list)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_set', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


    def __str__(self):
        return self.username
    

class EmailVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email verification for {self.user.email}"