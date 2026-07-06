from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Chờ xử lý"),
        ("CONFIRMED", "Đã xác nhận"),
        ("SHIPPED", "Đang giao"),
        ("DELIVERED", "Đã giao"),
        ("CANCELLED", "Đã hủy"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Tài khoản mua hàng"
    )
    full_name = models.CharField(max_length=200, verbose_name="Họ và tên")
    phone_number = models.CharField(max_length=15, verbose_name="Số điện thoại")
    shipping_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    total_price = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Tổng tiền (VND)")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="PENDING",
        verbose_name="Trạng thái"
    )
    shipping_provider = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Đơn vị vận chuyển"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.full_name} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Đơn hàng"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Sản phẩm"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Số lượng")
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Đơn giá lúc mua")
    batch = models.ForeignKey(
        "products.Batch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name="Lô sản phẩm"
    )
    
    ITEM_STATUS_CHOICES = (
        ("PENDING", "Chờ duyệt"),
        ("APPROVED", "Đã duyệt"),
        ("REJECTED", "Từ chối"),
    )
    status = models.CharField(
        max_length=20,
        choices=ITEM_STATUS_CHOICES,
        default="PENDING",
        verbose_name="Trạng thái duyệt"
    )

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"







