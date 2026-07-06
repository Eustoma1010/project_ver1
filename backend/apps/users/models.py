from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("BUYER", "Người mua"),
        ("FARMER", "Nông dân / Nhà sản xuất"),
        ("AUDITOR", "Kiểm định viên / Auditor"),
        ("ADMIN", "Quản trị viên"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="BUYER")
    phone_validator = RegexValidator(
        regex=r'^0\d{9,10}$',
        message="Số điện thoại phải bắt đầu bằng số 0 và gồm 10 hoặc 11 chữ số."
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[phone_validator],
        verbose_name="Số điện thoại"
    )
    address = models.TextField(blank=True, verbose_name="Địa chỉ")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

