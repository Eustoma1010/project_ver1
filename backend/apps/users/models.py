from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("BUYER", "Người mua"),
        ("FARMER", "Nông dân / Nhà sản xuất"),
        ("ADMIN", "Quản trị viên"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="BUYER")
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

