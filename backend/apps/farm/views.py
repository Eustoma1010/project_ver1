import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from apps.products.models import Farm, Product, Category, Batch, BatchMilestone, FarmAudit
from apps.orders.models import Order, OrderItem
from .forms import FarmRegistrationForm, ProductForm
from .blockchain import register_batch_on_blockchain, add_milestone_on_blockchain, record_delivery_on_blockchain

def get_clean_id(request, field_name):
    val = request.POST.get(field_name)
    if val:
        return str(val).replace(".", "").replace(",", "").strip()
    return None

def check_farm_approved(request):
    try:
        farm = Farm.objects.get(owner=request.user)
    except Farm.DoesNotExist:
        messages.error(request, "Bạn chưa đăng ký nhà cung cấp.")
        return None, redirect("farm:home")
        
    if farm.status == "SUSPENDED":
        messages.error(request, "Tài khoản doanh nghiệp của bạn đang bị đình chỉ hoạt động.")
        return None, redirect("farm:dashboard")
    elif farm.status != "APPROVED":
        messages.error(request, "Tài khoản doanh nghiệp của bạn chưa được duyệt.")
        return None, redirect("farm:home")
        
    return farm, None

@login_required
def home(request):
    """Handle farm page for all users.

    - If the user does not have a Farm, show registration form.
    - If the user has a Farm but not approved, show pending approval message.
    - If approved, show the farmer dashboard.
    """
    try:
        farm = Farm.objects.get(owner=request.user)
    except Farm.DoesNotExist:
        farm = None

    if farm is None:
        # No farm yet – render registration form
        if request.method == "POST":
            form = FarmRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                new_farm = form.save(commit=False)
                new_farm.owner = request.user
                
                # If a file was uploaded, save it and set the image_url
                if request.FILES.get("image_file"):
                    uploaded_file = request.FILES["image_file"]
                    saved_path = default_storage.save(f"farms/{uploaded_file.name}", uploaded_file)
                    new_farm.image_url = default_storage.url(saved_path)
                
                new_farm.save()
                messages.success(request, "Đăng ký đối tác thành công, hồ sơ đang chờ duyệt.")
                return redirect("farm:home")
        else:
            form = FarmRegistrationForm()
        return render(request, "farm/register.html", {"form": form})
    else:
        if farm.status in ["APPROVED", "SUSPENDED"]:
            # Approved or suspended (for legacy orders) - show dashboard
            return redirect("farm:dashboard")
        elif farm.status == "REJECTED":
            # Rejected - allow re-submitting with pre-filled form
            if request.method == "POST":
                form = FarmRegistrationForm(request.POST, request.FILES, instance=farm)
                if form.is_valid():
                    updated_farm = form.save(commit=False)
                    updated_farm.status = "PENDING_ADMIN"  # Reset status to Step 1
                    
                    if request.FILES.get("image_file"):
                        uploaded_file = request.FILES["image_file"]
                        saved_path = default_storage.save(f"farms/{uploaded_file.name}", uploaded_file)
                        updated_farm.image_url = default_storage.url(saved_path)
                        
                    updated_farm.save()
                    messages.success(request, "Gửi lại hồ sơ đăng ký đối tác thành công. Đang chờ duyệt sơ bộ.")
                    return redirect("farm:home")
            else:
                form = FarmRegistrationForm(instance=farm)
            return render(request, "farm/register.html", {
                "form": form,
                "farm": farm,
                "status_rejected": True
            })
        else:
            # PENDING_ADMIN, PENDING_AUDITOR
            return render(request, "farm/register.html", {
                "farm": farm,
                "status_pending": True
            })


@login_required
def dashboard(request):
    """Dashboard for approved or suspended farmer."""
    try:
        farm = Farm.objects.get(owner=request.user, status__in=["APPROVED", "SUSPENDED"])
    except Farm.DoesNotExist:
        messages.error(request, "Bạn chưa có nhà cung cấp được duyệt.")
        return redirect("farm:home")
        
    suspended = (farm.status == "SUSPENDED")
        
    # Handle forms
    if request.method == "POST":
        if "update_settings" in request.POST:
            if suspended:
                messages.error(request, "Tài khoản đang bị đình chỉ hoạt động. Không thể cập nhật thông tin.")
                return redirect("farm:dashboard")
            form = FarmRegistrationForm(request.POST, request.FILES, instance=farm)
            if form.is_valid():
                farm = form.save(commit=False)
                
                # Handle logo upload
                image_file = request.FILES.get('image_file')
                if image_file:
                    file_name = default_storage.save('farms/' + image_file.name, image_file)
                    farm.image_url = settings.MEDIA_URL + file_name
                    
                farm.save()
                messages.success(request, "Cập nhật cài đặt doanh nghiệp thành công!")
                return redirect("farm:dashboard")
        elif "update_item_status" in request.POST:
            item_id = get_clean_id(request, "item_id")
            new_status = request.POST.get("status")  # APPROVED or REJECTED
            
            # Fetch the order item belonging to the supplier's farm
            order_item = get_object_or_404(OrderItem, pk=item_id, product__farm=farm)
            order_item.status = new_status
            order_item.save()
            
            messages.success(request, f"Đã cập nhật trạng thái duyệt cho '{order_item.product.name}' thành công!")
            
            # Check if all items in this order are now approved
            order = order_item.order
            all_items = order.items.all()
            if all(item.status == "APPROVED" for item in all_items):
                order.status = "SHIPPED"
                order.save()
                messages.success(request, f"Đơn hàng #{order.id} đã được tất cả nhà cung cấp duyệt và tự động chuyển giao cho đơn vị vận chuyển '{order.shipping_provider}'!")
            
            return redirect("farm:dashboard")
        
        elif "update_order_status" in request.POST:
            order_id = get_clean_id(request, "order_id")
            new_status = request.POST.get("order_status")  # DELIVERED
            
            order = get_object_or_404(Order, pk=order_id)
            # Kiểm tra quyền: farmer chỉ có thể cập nhật đơn có sản phẩm của mình
            if not order.items.filter(product__farm=farm).exists():
                messages.error(request, "Bạn không có quyền cập nhật đơn hàng này.")
                return redirect("farm:dashboard")
            
            if new_status == "DELIVERED":
                order.status = "DELIVERED"
                order.save()
                
                # Ghi nhận mã băm SHA-256 bảo mật giao nhận lên Blockchain
                for item in order.items.all():
                    if item.batch:
                        try:
                            record_delivery_on_blockchain(
                                item.batch.batch_number,
                                str(order.id),
                                order.full_name,
                                order.shipping_address,
                                order.phone_number
                            )
                        except Exception as e:
                            print(f"Lỗi ghi nhận giao vận Blockchain cho đơn #{order.id}: {e}")
                
                messages.success(request, f"Đơn hàng #{order.id} đã giao thành công! Mã băm bảo mật đã được ghi nhận trên Blockchain.")
            
            return redirect("farm:dashboard")
            
    form = FarmRegistrationForm(instance=farm)
    order_items = OrderItem.objects.filter(product__farm=farm).select_related('order', 'product').order_by('-order__created_at')
    
    # Group items by order for cleaner display
    orders_dict = {}
    for item in order_items:
        o = item.order
        if o.id not in orders_dict:
            orders_dict[o.id] = {
                'order': o,
                'items': [],
                'subtotal': 0
            }
        item.total_price = item.price * item.quantity
        orders_dict[o.id]['items'].append(item)
        orders_dict[o.id]['subtotal'] += item.total_price
        
    context = {
        "farm": farm,
        "form": form,
        "orders": orders_dict.values(),
        "suspended": suspended,
    }
    return render(request, "farm/dashboard.html", context)


@login_required
def admin_reports(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
        
    # Handle approve/reject actions
    if request.method == "POST":
        action = request.POST.get("action")
        
        farm_id = get_clean_id(request, "farm_id")
        product_id = get_clean_id(request, "product_id")
        
        # Farm actions
        if action == "approve" and farm_id:
            farm = get_object_or_404(Farm, pk=farm_id)
            farm.status = "PENDING_AUDITOR"
            farm.save()
            # Upgrade user role
            owner = farm.owner
            owner.role = "FARMER"
            owner.save()
            messages.success(request, f"Đã duyệt sơ bộ hành chính cho '{farm.name}'. Hồ sơ đã chuyển sang Kiểm định viên thẩm định.")
        elif action == "reject" and farm_id:
            farm = get_object_or_404(Farm, pk=farm_id)
            farm.status = "REJECTED"
            farm.save()
            messages.success(request, f"Đã từ chối hồ sơ đăng ký của '{farm.name}'!")
            
        # Product actions
        elif action == "approve_product" and product_id:
            product = get_object_or_404(Product, pk=product_id)
            product.status = "PENDING_AUDITOR"
            product.save()
            messages.success(request, f"Đã duyệt sơ bộ sản phẩm '{product.name}'. Đã chuyển sang Kiểm định viên thẩm định.")
        elif action == "reject_product" and product_id:
            product = get_object_or_404(Product, pk=product_id)
            product.status = "REJECTED"
            product.save()
            messages.success(request, f"Đã từ chối duyệt sản phẩm '{product.name}'!")
            
        elif action == "approve_all_products":
            product_ids_str = request.POST.get("product_ids", "")
            if product_ids_str:
                product_ids = [int(x.strip()) for x in product_ids_str.split(",") if x.strip()]
                products = Product.objects.filter(pk__in=product_ids, status="PENDING_ADMIN")
                count = 0
                for product in products:
                    product.status = "PENDING_AUDITOR"
                    product.save()
                    count += 1
                if count > 0:
                    messages.success(request, f"Đã duyệt sơ bộ hàng loạt {count} sản phẩm thành công!")
            
        return redirect("admin-reports")

    total_farms = Farm.objects.count()
    pending_farms = Farm.objects.filter(status="PENDING_ADMIN").count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.exclude(status='CANCELLED').aggregate(sum=Sum('total_price'))['sum'] or 0

    pending_farms_list = Farm.objects.filter(status="PENDING_ADMIN").select_related('owner')
    approved_farms_list = Farm.objects.filter(status="APPROVED").select_related('owner')
    pending_products_list = Product.objects.filter(status="PENDING_ADMIN").select_related('farm')
    recent_orders = Order.objects.all().order_by('-created_at')[:10]

    context = {
        'total_farms': total_farms,
        'pending_farms': pending_farms,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_farms_list': pending_farms_list,
        'approved_farms_list': approved_farms_list,
        'pending_products_list': pending_products_list,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/reports.html', context)


@login_required
def products(request):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
    
    products_list = farm.products.all()
    return render(request, "farm/products.html", {"farm": farm, "products": products_list})


@login_required
def add_product(request):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farm = farm
            product.origin = farm.province if farm.province else farm.region
            
            # Handle uploaded image from device
            image_file = request.FILES.get('image_file')
            if image_file:
                file_name = default_storage.save('products/' + image_file.name, image_file)
                product.image_url = settings.MEDIA_URL + file_name
            
            # Generate unique slug
            slug = slugify(product.name)
            if not slug:
                slug = str(uuid.uuid4())[:8]
            else:
                if Product.objects.filter(slug=slug).exists():
                    slug = f"{slug}-{str(uuid.uuid4())[:8]}"
            product.slug = slug
            product.save()
            messages.success(request, "Thêm sản phẩm thành công!")
            return redirect("farm:products")
    else:
        form = ProductForm()
    return render(request, "farm/product_form.html", {"form": form, "title": "Thêm Sản Phẩm", "farm": farm})


@login_required
def edit_product(request, pk):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    product = get_object_or_404(Product, pk=pk, farm=farm)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.origin = farm.province if farm.province else farm.region
            
            # Handle uploaded image from device
            image_file = request.FILES.get('image_file')
            if image_file:
                file_name = default_storage.save('products/' + image_file.name, image_file)
                product.image_url = settings.MEDIA_URL + file_name
                
            # Re-generate slug if name changed
            slug = slugify(product.name)
            if not slug:
                slug = str(uuid.uuid4())[:8]
            else:
                if Product.objects.filter(slug=slug).exclude(pk=pk).exists():
                    slug = f"{slug}-{str(uuid.uuid4())[:8]}"
            product.slug = slug
            product.save()
            messages.success(request, "Cập nhật sản phẩm thành công!")
            return redirect("farm:products")
    else:
        form = ProductForm(instance=product)
    return render(request, "farm/product_form.html", {"form": form, "title": "Chỉnh Sửa Sản Phẩm", "farm": farm, "product": product})


@login_required
def delete_product(request, pk):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    product = get_object_or_404(Product, pk=pk, farm=farm)
    product.delete()
    messages.success(request, "Đã xóa sản phẩm thành công!")
    return redirect("farm:products")


@login_required
def batches_list(request):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    batches = Batch.objects.filter(product__farm=farm).select_related('product').order_by('-created_at')
    return render(request, "farm/batches.html", {"batches": batches, "farm": farm})


@login_required
def add_batch(request):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    products = Product.objects.filter(farm=farm, status='APPROVED')
    
    if request.method == "POST":
        product_id = request.POST.get("product")
        batch_number = request.POST.get("batch_number").strip()
        initial_quantity = int(request.POST.get("initial_quantity", 0))
        seeding_date = request.POST.get("seeding_date")
        
        product = get_object_or_404(Product, pk=product_id, farm=farm)
        
        if Batch.objects.filter(batch_number=batch_number).exists():
            messages.error(request, f"Mã số lô hàng '{batch_number}' đã tồn tại trên hệ thống!")
        else:
            # 1. Đăng ký lô hàng lên Blockchain trước
            tx_hash = register_batch_on_blockchain(batch_number, product.name, farm.name)
            
            # 2. Lưu vào CSDL nội bộ
            batch = Batch.objects.create(
                product=product,
                batch_number=batch_number,
                initial_quantity=initial_quantity,
                remaining_quantity=initial_quantity,
                status="CULTIVATING",
                seeding_date=seeding_date,
                blockchain_tx_hash=tx_hash
            )
            
            # Mốc khởi tạo chuẩn hóa (Ủy thác cho từng lô hàng / sản phẩm tự do thiết kế các mốc sau)
            init_title = "Khởi tạo lô sản xuất/gieo trồng"
            init_desc = f"Khởi tạo chu kỳ sản xuất & gieo trồng mới cho sản phẩm {product.name} tại hệ thống truy xuất nguồn gốc."
            
            # 3. Tạo mốc lịch sử đầu tiên (Mốc khởi tạo hệ thống tự duyệt)
            ms_tx_hash = add_milestone_on_blockchain(
                batch_number,
                init_title,
                init_desc,
                farm.province if farm.province else farm.region,
                farm.name
            )
            BatchMilestone.objects.create(
                batch=batch,
                title=init_title,
                description=init_desc,
                location=farm.province if farm.province else farm.region,
                actor=farm.name,
                status="VERIFIED",
                blockchain_tx_hash=ms_tx_hash
            )
            
            messages.success(request, f"Đã khởi tạo lô hàng {batch_number} thành công và lưu vết khởi đầu lên Blockchain!")
            return redirect("farm:batches")
            
    return render(request, "farm/batch_form.html", {"products": products, "farm": farm, "title": "Khởi Tạo Lô Sản Xuất & Canh Tác"})


@login_required
def add_milestone(request, batch_id):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    batch = get_object_or_404(Batch, pk=batch_id, product__farm=farm)
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title == "custom":
            title = request.POST.get("custom_title", "").strip()
        description = request.POST.get("description").strip()
        location = request.POST.get("location").strip()
        actor = request.POST.get("actor").strip()
        
        # Parse parameters based on product category
        parameters = {}
        category_slug = batch.product.category.slug if batch.product.category else "other"
        if category_slug == 'sua':
            parameters = {
                "storage_temp": request.POST.get("param_storage_temp", "").strip(),
                "ph_level": request.POST.get("param_ph_level", "").strip(),
                "fat_content": request.POST.get("param_fat_content", "").strip(),
                "bacteria_count": request.POST.get("param_bacteria_count", "").strip(),
            }
        elif category_slug in ['ca-phe', 'tra']:
            parameters = {
                "moisture": request.POST.get("param_moisture", "").strip(),
                "roast_temp": request.POST.get("param_roast_temp", "").strip(),
                "altitude": request.POST.get("param_altitude", "").strip(),
                "roast_note": request.POST.get("param_roast_note", "").strip(),
            }
        else:
            parameters = {
                "soil_temp": request.POST.get("param_soil_temp", "").strip(),
                "soil_moisture": request.POST.get("param_soil_moisture", "").strip(),
                "ph_level": request.POST.get("param_ph_level", "").strip(),
                "fertilizer": request.POST.get("param_fertilizer", "").strip(),
            }
        # Filter empty values
        parameters = {k: v for k, v in parameters.items() if v}
        
        blockchain_description = description
        if parameters:
            param_labels = {
                "storage_temp": "Nhiệt độ bảo quản",
                "ph_level": "Độ pH",
                "fat_content": "Hàm lượng béo",
                "bacteria_count": "Tỷ lệ vi sinh",
                "moisture": "Độ ẩm hạt",
                "roast_temp": "Nhiệt độ rang/sấy",
                "altitude": "Độ cao canh tác",
                "roast_note": "Ghi chú rang/sấy",
                "soil_temp": "Nhiệt độ đất",
                "soil_moisture": "Độ ẩm đất",
                "fertilizer": "Phân bón sử dụng",
            }
            param_lines = [f"- {param_labels.get(k, k)}: {v}" for k, v in parameters.items()]
            blockchain_description += "\n\n[Thông số kỹ thuật]\n" + "\n".join(param_lines)
            
        # 1. Lưu mốc canh tác vào CSDL dưới dạng PENDING_AUDIT (chưa ghi Blockchain)
        BatchMilestone.objects.create(
            batch=batch,
            title=title,
            description=description,
            location=location,
            actor=actor,
            status="PENDING_AUDIT",
            milestone_type="MANUAL",
            blockchain_tx_hash=None,
            parameters=parameters
        )
        
        messages.success(request, f"Đã thêm mốc nhật ký '{title}' thành công! Hồ sơ đang chờ Kiểm định viên xác duyệt để ghi nhận lên Blockchain.")
        return redirect("farm:batches")
        
    suggested_milestones = [
        "Nhập nguyên liệu thô",
        "Gieo hạt & Xuống giống",
        "Chăm sóc & Nuôi dưỡng",
        "Tiệt trùng & Chế biến",
        "Kiểm nghiệm chất lượng (Lab Test)",
        "Thu hoạch sản phẩm",
        "Đóng gói & Dán nhãn",
        "Kiểm định an toàn thực phẩm"
    ]
        
    return render(request, "farm/milestone_form.html", {
        "batch": batch,
        "farm": farm,
        "suggested_milestones": suggested_milestones
    })


@login_required
def harvest_batch(request, batch_id):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    batch = get_object_or_404(Batch, pk=batch_id, product__farm=farm)
    
    if request.method == "POST":
        harvest_date = request.POST.get("harvest_date")
        
        # 1. Tạo mốc lịch sử ở DB dưới dạng PENDING_AUDIT (để khi duyệt sẽ kích hoạt HARVESTED và ghi Blockchain)
        BatchMilestone.objects.create(
            batch=batch,
            title="Thu hoạch & Đóng gói",
            description=f"Đã hoàn thành thu hoạch nông sản tươi đạt chuẩn organic, sơ chế và đóng gói đưa lên sàn.",
            location=farm.province if farm.province else farm.region,
            actor=farm.name,
            status="PENDING_AUDIT",
            milestone_type="MANUAL",
            blockchain_tx_hash=None,
            parameters={"harvest_date": harvest_date}
        )
        
        messages.success(request, f"Đã gửi yêu cầu xác nhận thu hoạch cho lô hàng {batch.batch_number}! Vui lòng chờ Kiểm định viên xác duyệt để bắt đầu mở bán.")
        return redirect("farm:batches")
        
    return render(request, "farm/harvest_form.html", {"batch": batch, "farm": farm})

@login_required
def simulate_iot(request, batch_id):
    farm, error_redirect = check_farm_approved(request)
    if error_redirect:
        return error_redirect
        
    batch = get_object_or_404(Batch, pk=batch_id, product__farm=farm)
    
    # Generate random IoT reading
    import random
    temp = round(random.uniform(22.0, 26.5), 1)
    humidity = round(random.uniform(65.0, 78.0), 1)
    soil_ph = round(random.uniform(6.2, 6.8), 1)
    
    title = "Cập nhật cảm biến IoT tự động"
    description = f"Thiết bị cảm biến thông minh IoT ghi nhận các chỉ số sinh trưởng khách quan tại vườn trồng của lô {batch.batch_number}."
    parameters = {
        "soil_temp": f"{temp}°C",
        "soil_moisture": f"{humidity}%",
        "ph_level": str(soil_ph)
    }
    
    blockchain_description = f"{description}\n\n[Thông số kỹ thuật cảm biến]\n- Nhiệt độ đất: {temp}°C\n- Độ ẩm đất: {humidity}%\n- Độ pH đất: {soil_ph}"
    
    # IoT data is trusted and verified immediately -> write straight to Blockchain
    try:
        tx_hash = add_milestone_on_blockchain(
            batch.batch_number,
            title,
            blockchain_description,
            farm.province if farm.province else farm.region,
            "Cảm biến IoT (Tự động)"
        )
    except Exception as e:
        messages.error(request, f"Lỗi kết nối Blockchain khi gửi dữ liệu IoT: {e}")
        return redirect("farm:batches")
        
    # Save directly as VERIFIED
    BatchMilestone.objects.create(
        batch=batch,
        title=title,
        description=description,
        location=farm.province if farm.province else farm.region,
        actor="Cảm biến IoT (Tự động)",
        status="VERIFIED",
        milestone_type="IOT",
        blockchain_tx_hash=tx_hash,
        parameters=parameters
    )
    
    messages.success(request, f"Dữ liệu cảm biến IoT của lô {batch.batch_number} đã được ghi nhận tự động lên Blockchain thành công!")
    return redirect("farm:batches")

@login_required
def auditor_dashboard(request):
    import datetime
    from django.http import HttpResponseForbidden
    
    if request.user.role != "AUDITOR" and not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
        
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "approve_farm":
            farm_id = get_clean_id(request, "farm_id")
            farm = get_object_or_404(Farm, pk=farm_id)
            farm.status = "APPROVED"
            farm.last_audit_date = datetime.date.today()
            farm.next_audit_deadline = datetime.date.today() + datetime.timedelta(days=180)
            farm.save()
            messages.success(request, f"Đã duyệt và cấp chứng chỉ cho nhà cung cấp '{farm.name}' thành công!")
            return redirect("farm:auditor_dashboard")
            
        elif action == "reject_farm":
            farm_id = get_clean_id(request, "farm_id")
            farm = get_object_or_404(Farm, pk=farm_id)
            farm.status = "REJECTED"
            farm.save()
            messages.success(request, f"Đã từ chối cấp chứng chỉ cho nhà cung cấp '{farm.name}'!")
            return redirect("farm:auditor_dashboard")
            
        elif action == "audit_farm":
            farm_id = get_clean_id(request, "farm_id")
            result = request.POST.get("result") == "pass"
            notes = request.POST.get("notes", "").strip()
            
            farm = get_object_or_404(Farm, pk=farm_id)
            
            # Record audit history
            FarmAudit.objects.create(
                farm=farm,
                auditor=request.user,
                result=result,
                notes=notes
            )
            
            if result:
                farm.status = "APPROVED"
                farm.last_audit_date = datetime.date.today()
                farm.next_audit_deadline = datetime.date.today() + datetime.timedelta(days=180)
                farm.save()
                messages.success(request, f"Đợt kiểm tra thành công. '{farm.name}' tiếp tục duy trì trạng thái HOẠT ĐỘNG.")
            else:
                farm.status = "SUSPENDED"
                farm.save()
                messages.warning(request, f"Cảnh báo: '{farm.name}' không đạt kiểm định và đã bị ĐÌNH CHỈ hoạt động!")
                
            return redirect("farm:auditor_dashboard")
            
        elif action == "verify_milestone":
            milestone_id = get_clean_id(request, "milestone_id")
            inspection_id = request.POST.get("inspection_id", "").strip()
            audit_opinion = request.POST.get("audit_opinion", "").strip()
            
            milestone = get_object_or_404(BatchMilestone, pk=milestone_id)
            batch = milestone.batch
            farm = batch.product.farm
            
            try:
                # Compile parameters for blockchain writing
                blockchain_description = milestone.description
                if milestone.parameters:
                    param_labels = {
                        "storage_temp": "Nhiệt độ bảo quản",
                        "ph_level": "Độ pH",
                        "fat_content": "Hàm lượng béo",
                        "bacteria_count": "Tỷ lệ vi sinh",
                        "moisture": "Độ ẩm hạt",
                        "roast_temp": "Nhiệt độ rang/sấy",
                        "altitude": "Độ cao canh tác",
                        "roast_note": "Ghi chú rang/sấy",
                        "soil_temp": "Nhiệt độ đất",
                        "soil_moisture": "Độ ẩm đất",
                        "fertilizer": "Phân bón sử dụng",
                        "harvest_date": "Ngày thu hoạch"
                    }
                    param_lines = [f"- {param_labels.get(k, k)}: {v}" for k, v in milestone.parameters.items()]
                    blockchain_description += "\n\n[Thông số kỹ thuật]\n" + "\n".join(param_lines)
                
                # Write to local blockchain
                tx_hash = add_milestone_on_blockchain(
                    batch.batch_number,
                    milestone.title,
                    blockchain_description,
                    milestone.location,
                    f"{milestone.actor} (Xác thực: {request.user.username})"
                )
                
                # If Thu hoạch milestone -> activate HARVESTED status for the batch
                if milestone.title == "Thu hoạch & Đóng gói":
                    batch.status = "HARVESTED"
                    harvest_date = milestone.parameters.get("harvest_date")
                    if harvest_date:
                        batch.harvest_date = harvest_date
                    batch.save()
                    
                milestone.status = "VERIFIED"
                milestone.blockchain_tx_hash = tx_hash
                milestone.auditor = request.user
                milestone.inspection_id = inspection_id
                milestone.audit_opinion = audit_opinion
                milestone.save()
                milestone.batch.product.update_availability()
                
                messages.success(request, f"Đã xác thực cột mốc '{milestone.title}' và ghi nhận thành công lên Blockchain!")
            except Exception as e:
                messages.error(request, f"Lỗi ghi Blockchain: {e}")
                
            return redirect("farm:auditor_dashboard")
            
        elif action == "reject_milestone":
            milestone_id = get_clean_id(request, "milestone_id")
            inspection_id = request.POST.get("inspection_id", "").strip()
            audit_opinion = request.POST.get("audit_opinion", "").strip()
            
            milestone = get_object_or_404(BatchMilestone, pk=milestone_id)
            milestone.status = "REJECTED"
            milestone.auditor = request.user
            milestone.inspection_id = inspection_id
            milestone.audit_opinion = audit_opinion
            milestone.save()
            milestone.batch.product.update_availability()
            
            messages.warning(request, f"Đã từ chối cột mốc '{milestone.title}' của lô {milestone.batch.batch_number}!")
            return redirect("farm:auditor_dashboard")
            
        elif action == "approve_all_milestones":
            milestone_ids_str = request.POST.get("milestone_ids", "")
            if milestone_ids_str:
                milestone_ids = [int(x.strip()) for x in milestone_ids_str.split(",") if x.strip()]
                milestones = BatchMilestone.objects.filter(pk__in=milestone_ids, status="PENDING_AUDIT")
                
                success_count = 0
                error_count = 0
                
                for milestone in milestones:
                    batch = milestone.batch
                    farm = batch.product.farm
                    
                    try:
                        # Compile parameters for blockchain writing
                        blockchain_description = milestone.description
                        if milestone.parameters:
                            param_labels = {
                                "storage_temp": "Nhiệt độ bảo quản",
                                "ph_level": "Độ pH",
                                "fat_content": "Hàm lượng béo",
                                "bacteria_count": "Tỷ lệ vi sinh",
                                "moisture": "Độ ẩm hạt",
                                "roast_temp": "Nhiệt độ rang/sấy",
                                "altitude": "Độ cao canh tác",
                                "roast_note": "Ghi chú rang/sấy",
                                "soil_temp": "Nhiệt độ đất",
                                "soil_moisture": "Độ ẩm đất",
                                "fertilizer": "Phân bón sử dụng",
                                "harvest_date": "Ngày thu hoạch"
                            }
                            param_lines = [f"- {param_labels.get(k, k)}: {v}" for k, v in milestone.parameters.items()]
                            blockchain_description += "\n\n[Thông số kỹ thuật]\n" + "\n".join(param_lines)
                        
                        # Generate auto inspection ID
                        import random
                        auto_insp_id = f"AUTO-INSP-{random.randint(1000, 9999)}"
                        
                        # Write to local blockchain
                        tx_hash = add_milestone_on_blockchain(
                            batch.batch_number,
                            milestone.title,
                            blockchain_description,
                            milestone.location,
                            f"{milestone.actor} (Xác thực hàng loạt: {request.user.username})"
                        )
                        
                        # If Thu hoạch milestone -> activate HARVESTED status for the batch
                        if milestone.title == "Thu hoạch & Đóng gói":
                            batch.status = "HARVESTED"
                            harvest_date = milestone.parameters.get("harvest_date")
                            if harvest_date:
                                batch.harvest_date = harvest_date
                            batch.save()
                            
                        milestone.status = "VERIFIED"
                        milestone.blockchain_tx_hash = tx_hash
                        milestone.auditor = request.user
                        milestone.inspection_id = auto_insp_id
                        milestone.audit_opinion = "Phê duyệt hàng loạt."
                        milestone.save()
                        milestone.batch.product.update_availability()
                        
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        
                if success_count > 0:
                    messages.success(request, f"Đã duyệt hàng loạt {success_count} cột mốc lên Blockchain thành công!")
                if error_count > 0:
                    messages.error(request, f"Gặp lỗi khi ghi Blockchain cho {error_count} cột mốc.")
                    
            return redirect("farm:auditor_dashboard")
            
        elif action == "approve_product":
            product_id = get_clean_id(request, "product_id")
            product = get_object_or_404(Product, pk=product_id)
            product.status = "APPROVED"
            product.save()
            messages.success(request, f"Đã phê duyệt sản phẩm '{product.name}' của nông trại '{product.farm.name}' thành công!")
            return redirect("farm:auditor_dashboard")
            
        elif action == "reject_product":
            product_id = get_clean_id(request, "product_id")
            product = get_object_or_404(Product, pk=product_id)
            product.status = "REJECTED"
            product.save()
            messages.success(request, f"Đã từ chối phê duyệt sản phẩm '{product.name}'!")
            return redirect("farm:auditor_dashboard")
            
        elif action == "approve_all_products":
            product_ids_str = request.POST.get("product_ids", "")
            if product_ids_str:
                product_ids = [int(x.strip()) for x in product_ids_str.split(",") if x.strip()]
                products = Product.objects.filter(pk__in=product_ids, status="PENDING_AUDITOR")
                count = 0
                for product in products:
                    product.status = "APPROVED"
                    product.save()
                    count += 1
                if count > 0:
                    messages.success(request, f"Đã phê duyệt hàng loạt {count} sản phẩm thành công!")
            return redirect("farm:auditor_dashboard")
            
    # Queries for GET
    pending_farms = Farm.objects.filter(status="PENDING_AUDITOR").select_related('owner')
    active_farms = Farm.objects.filter(status__in=["APPROVED", "SUSPENDED"]).select_related('owner')
    pending_milestones = BatchMilestone.objects.filter(status="PENDING_AUDIT", batch__product__status="APPROVED").select_related('batch__product__farm')
    pending_products = Product.objects.filter(status="PENDING_AUDITOR").select_related('farm')
    recent_audits = FarmAudit.objects.all().select_related('farm', 'auditor')[:15]
    
    context = {
        "pending_farms": pending_farms,
        "active_farms": active_farms,
        "pending_milestones": pending_milestones,
        "pending_products": pending_products,
        "recent_audits": recent_audits,
    }
    return render(request, "farm/auditor_dashboard.html", context)
