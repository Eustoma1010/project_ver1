import json
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from apps.products.models import Product, Batch


def allocate_batch_fifo(product, quantity):
    """
    Phân bổ hàng tồn kho theo nguyên tắc FIFO (First In, First Out).
    Trả về danh sách các tuple (batch, allocated_qty) cho sản phẩm yêu cầu.
    Nếu tổng tồn kho không đủ, trả về None.
    """
    batches = Batch.objects.filter(
        product=product,
        status="HARVESTED",
        remaining_quantity__gt=0
    ).order_by("harvest_date", "seeding_date")

    allocations = []
    remaining_need = quantity

    for batch in batches:
        if remaining_need <= 0:
            break
        alloc = min(batch.remaining_quantity, remaining_need)
        allocations.append((batch, alloc))
        remaining_need -= alloc

    if remaining_need > 0:
        return None  # Không đủ hàng tồn kho

    return allocations


def checkout(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        shipping_address = request.POST.get("shipping_address")
        shipping_provider = request.POST.get("shipping_provider", "Viettel Post")
        cart_data_raw = request.POST.get("cart_data")

        if not cart_data_raw:
            messages.error(request, "Giỏ hàng của bạn đang trống.")
            return redirect("home")

        try:
            cart_items = json.loads(cart_data_raw)
            if not cart_items:
                messages.error(request, "Giỏ hàng của bạn đang trống.")
                return redirect("home")

            # Sử dụng transaction.atomic để đảm bảo tính toàn vẹn dữ liệu
            with transaction.atomic():
                # 1. Kiểm tra tồn kho FIFO cho tất cả sản phẩm trước khi tạo đơn
                all_allocations = []
                for item in cart_items:
                    product_id = item.get("id")
                    quantity = int(item.get("quantity", 1))
                    product = Product.objects.get(id=product_id)

                    allocations = allocate_batch_fifo(product, quantity)
                    if allocations is None:
                        active_batch = product.active_batch
                        available = active_batch.remaining_quantity if active_batch else 0
                        messages.error(
                            request,
                            f"Sản phẩm '{product.name}' không đủ hàng tồn kho. "
                            f"Hiện chỉ còn {available} {product.unit} trong kho."
                        )
                        return redirect("home")

                    all_allocations.append((product, quantity, allocations))

                # 2. Tạo đơn hàng
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    full_name=full_name,
                    phone_number=phone_number,
                    shipping_address=shipping_address,
                    shipping_provider=shipping_provider,
                    total_price=0
                )

                # 3. Tạo OrderItem và trừ kho FIFO
                total = 0
                for product, quantity, allocations in all_allocations:
                    for batch, alloc_qty in allocations:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=alloc_qty,
                            price=product.price,
                            batch=batch
                        )
                        total += product.price * alloc_qty

                        # Trừ kho lô hàng
                        batch.remaining_quantity -= alloc_qty
                        if batch.remaining_quantity <= 0:
                            batch.remaining_quantity = 0
                            batch.status = "OUT_OF_STOCK"
                        batch.save()

                # 4. Tính phí vận chuyển
                shipping_fee = 0 if total >= 200000 else 30000
                order.total_price = total + shipping_fee
                order.save()

            messages.success(request, "Đơn hàng của bạn đã được đặt thành công!")
            return redirect(f"/orders/success/?order_id={order.id}")

        except Product.DoesNotExist:
            messages.error(request, "Một sản phẩm trong giỏ hàng không tồn tại.")
            return redirect("home")
        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi trong quá trình đặt hàng: {str(e)}")
            return redirect("home")

    return redirect("home")


def success_view(request):
    order_id = request.GET.get("order_id")
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            pass
    return render(request, "orders/success.html", {"order": order})


@login_required(login_url="/users/login/")
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product', 'items__batch__milestones')
    return render(request, "orders/my_orders.html", {"orders": orders})
