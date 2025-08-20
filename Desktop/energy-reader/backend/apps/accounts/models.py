from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = [
        ('admin', 'Administrador'),
        ('officer', 'Officer'),
        ('partner', 'Parceiro'),
        ('client', 'Cliente'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"