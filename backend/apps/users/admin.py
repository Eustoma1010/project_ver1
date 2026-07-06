from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "role", "phone_number", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Thông tin bổ sung", {"fields": ("role", "phone_number", "address")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Thông tin bổ sung", {"fields": ("role", "phone_number", "address")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

