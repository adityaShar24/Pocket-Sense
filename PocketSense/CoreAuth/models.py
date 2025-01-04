from django.contrib.auth.models import AbstractUser# Create your models here.
from django.db import models

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