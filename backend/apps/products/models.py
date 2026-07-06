from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"

    def __str__(self):
        return self.name

class Farm(models.Model):
    STATUS_CHOICES = (
        ("PENDING_ADMIN", "Chờ Admin duyệt sơ bộ"),
        ("PENDING_AUDITOR", "Chờ Kiểm định viên duyệt"),
        ("APPROVED", "Đã duyệt & Cấp chứng chỉ"),
        ("REJECTED", "Bị từ chối"),
        ("SUSPENDED", "Bị đình chỉ hoạt động"),
    )
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3)],
        verbose_name="Tên nhà cung cấp"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="farms",
        verbose_name="Chủ doanh nghiệp"
    )
    region = models.CharField(max_length=100, verbose_name="Khu vực/Vùng miền")
    province = models.CharField(max_length=100, blank=True, verbose_name="Tỉnh/Thành phố")
    
    tax_code_validator = RegexValidator(
        regex=r'^\d{10}$|^\d{13}$|^\d{10}-\d{3}$',
        message="Mã số thuế phải gồm 10 chữ số hoặc 13 chữ số (ví dụ: 1234567890 hoặc 1234567890-123)."
    )
    tax_code = models.CharField(
        max_length=50,
        validators=[tax_code_validator],
        verbose_name="Mã số thuế"
    )
    
    phone_validator = RegexValidator(
        regex=r'^0\d{9,10}$',
        message="Số điện thoại liên hệ phải bắt đầu bằng số 0 và gồm 10 hoặc 11 chữ số."
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        verbose_name="Số điện thoại liên hệ"
    )
    email = models.EmailField(verbose_name="Email liên hệ")
    description = models.TextField(blank=True, verbose_name="Giới thiệu doanh nghiệp")
    approved = models.BooleanField(default=False, verbose_name="Được duyệt")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING_ADMIN",
        verbose_name="Trạng thái duyệt"
    )
    business_license = models.FileField(
        upload_to="licenses/",
        null=True,
        blank=False,
        verbose_name="Ảnh Giấy phép kinh doanh"
    )
    last_audit_date = models.DateField(null=True, blank=True, verbose_name="Ngày kiểm định gần nhất")
    next_audit_deadline = models.DateField(null=True, blank=True, verbose_name="Hạn kiểm định tiếp theo")
    image_url = models.URLField(max_length=500, blank=True, verbose_name="Link ảnh đại diện")

    class Meta:
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"

    def save(self, *args, **kwargs):
        if self.status == "APPROVED":
            self.approved = True
        else:
            self.approved = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class FarmAudit(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="audits", verbose_name="Nông trại")
    auditor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Kiểm định viên")
    audit_date = models.DateField(auto_now_add=True, verbose_name="Ngày kiểm định")
    result = models.BooleanField(verbose_name="Đạt yêu cầu")
    notes = models.TextField(blank=True, verbose_name="Ý kiến nhận xét/Đánh giá")

    class Meta:
        verbose_name = "Đánh giá nông trại"
        verbose_name_plural = "Đánh giá nông trại"
        ordering = ["-audit_date"]

    def __str__(self):
        return f"Đánh giá {self.farm.name} - {'Đạt' if self.result else 'Không đạt'}"

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Danh mục"
    )
    farm = models.ForeignKey(
        Farm,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Nông trại"
    )
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(unique=True)
    origin = models.CharField(max_length=200, verbose_name="Xuất xứ")
    price = models.IntegerField(validators=[MinValueValidator(1000)], verbose_name="Giá bán (VND)")
    unit = models.CharField(max_length=50, verbose_name="Đơn vị tính")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0, verbose_name="Đánh giá")
    reviews_count = models.IntegerField(default=0, verbose_name="Số lượng đánh giá")
    BADGE_CHOICES = (
        ("", "Không có"),
        ("Organic", "Organic"),
        ("Bán chạy", "Bán chạy"),
        ("VietGAP", "VietGAP"),
        ("Local", "Local"),
        ("Thuần chay", "Thuần chay"),
        ("Non-GMO", "Non-GMO"),
    )
    badge = models.CharField(
        max_length=50,
        choices=BADGE_CHOICES,
        blank=True,
        verbose_name="Nhãn (Badge)"
    )
    image_url = models.URLField(max_length=500, blank=True, verbose_name="Link ảnh sản phẩm")
    description = models.TextField(blank=True, verbose_name="Mô tả sản phẩm")
    available = models.BooleanField(default=False, verbose_name="Còn hàng")
    STATUS_CHOICES = (
        ("PENDING_ADMIN", "Chờ Admin duyệt"),
        ("PENDING_AUDITOR", "Chờ Kiểm định viên duyệt"),
        ("APPROVED", "Đã duyệt"),
        ("REJECTED", "Từ chối"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING_ADMIN",
        verbose_name="Trạng thái duyệt"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def active_batch(self):
        """Lấy lô hàng đã thu hoạch sớm nhất và vẫn còn tồn kho (FIFO), có mốc thu hoạch đã được xác thực."""
        return self.batches.filter(
            status="HARVESTED",
            remaining_quantity__gt=0,
            milestones__title="Thu hoạch & Đóng gói",
            milestones__status="VERIFIED"
        ).order_by("harvest_date").first()

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ["-created_at"]

    def update_availability(self):
        has_active = self.batches.filter(
            status="HARVESTED",
            remaining_quantity__gt=0,
            milestones__title="Thu hoạch & Đóng gói",
            milestones__status="VERIFIED"
        ).exists() if self.pk else False
        is_approved = (self.status == "APPROVED")
        new_avail = has_active and is_approved
        if self.available != new_avail:
            self.available = new_avail
            Product.objects.filter(pk=self.pk).update(available=new_avail)

    def save(self, *args, **kwargs):
        if self.farm:
            self.origin = self.farm.province if self.farm.province else self.farm.region
        else:
            self.origin = "Việt Nam"
        
        has_active = self.batches.filter(
            status="HARVESTED",
            remaining_quantity__gt=0,
            milestones__title="Thu hoạch & Đóng gói",
            milestones__status="VERIFIED"
        ).exists() if self.pk else False
        is_approved = (self.status == "APPROVED")
        self.available = has_active and is_approved
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Batch(models.Model):
    STATUS_CHOICES = (
        ("CULTIVATING", "Đang canh tác"),
        ("HARVESTED", "Đã thu hoạch (Sẵn sàng bán)"),
        ("OUT_OF_STOCK", "Hết hàng"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="batches",
        verbose_name="Sản phẩm"
    )
    batch_number = models.CharField(max_length=100, unique=True, verbose_name="Mã số lô hàng")
    initial_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Số lượng gieo giống ban đầu")
    remaining_quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name="Số lượng tồn kho của lô")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CULTIVATING")
    seeding_date = models.DateField(verbose_name="Ngày gieo giống")
    harvest_date = models.DateField(null=True, blank=True, verbose_name="Ngày thu hoạch")
    blockchain_tx_hash = models.CharField(max_length=66, blank=True, null=True, verbose_name="TxHash khởi tạo lô")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lô sản phẩm"
        verbose_name_plural = "Lô sản phẩm"
        ordering = ["harvest_date", "seeding_date"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.product:
            self.product.update_availability()

    def __str__(self):
        return f"Lô {self.batch_number} - {self.product.name} ({self.get_status_display()})"


class BatchMilestone(models.Model):
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="milestones",
        verbose_name="Lô sản phẩm"
    )
    title = models.CharField(max_length=100, verbose_name="Tiêu đề mốc")
    description = models.TextField(verbose_name="Mô tả kỹ thuật chăm sóc")
    location = models.CharField(max_length=200, verbose_name="Địa điểm thực hiện")
    actor = models.CharField(max_length=100, verbose_name="Người thực hiện")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian ghi nhận")
    blockchain_tx_hash = models.CharField(max_length=66, blank=True, null=True, verbose_name="TxHash cột mốc")
    parameters = models.JSONField(default=dict, blank=True, verbose_name="Thông số kỹ thuật")
    
    status = models.CharField(
        max_length=20,
        choices=(
            ("PENDING_AUDIT", "Chờ kiểm định"),
            ("VERIFIED", "Đã xác thực"),
            ("REJECTED", "Bị từ chối")
        ),
        default="PENDING_AUDIT",
        verbose_name="Trạng thái kiểm định"
    )
    milestone_type = models.CharField(
        max_length=10,
        choices=(
            ("MANUAL", "Thủ công"),
            ("IOT", "Tự động (IoT)")
        ),
        default="MANUAL",
        verbose_name="Loại nhật ký"
    )
    audit_opinion = models.TextField(blank=True, verbose_name="Ý kiến kiểm định")
    inspection_id = models.CharField(max_length=100, blank=True, verbose_name="Mã số biên bản kiểm thực")
    auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_milestones",
        verbose_name="Kiểm định viên"
    )

    class Meta:
        verbose_name = "Nhật ký lô hàng"
        verbose_name_plural = "Nhật ký lô hàng"
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.title} - Lô {self.batch.batch_number} ({self.get_status_display()})"


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục blog")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Danh mục blog"
        verbose_name_plural = "Danh mục blog"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Danh mục"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(unique=True)
    summary = models.TextField(verbose_name="Tóm tắt ngắn")
    content = models.TextField(verbose_name="Nội dung bài viết")
    image_url = models.URLField(max_length=500, blank=True, verbose_name="Link ảnh đại diện")
    published_date = models.DateField(auto_now_add=True, verbose_name="Ngày đăng")

    class Meta:
        verbose_name = "Bài viết blog"
        verbose_name_plural = "Bài viết blog"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

class FavoriteProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Người dùng"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Sản phẩm"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sản phẩm yêu thích"
        verbose_name_plural = "Sản phẩm yêu thích"
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
