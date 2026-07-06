from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Farm, Product, BlogPost, FavoriteProduct, Batch
from apps.users.models import CustomUser

from django.db.models import Case, When, Value, IntegerField

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(status='APPROVED', farm__status='APPROVED').annotate(
        priority=Case(
            When(badge="Bán chạy", then=Value(1)),
            When(badge="Organic", then=Value(2)),
            When(badge="VietGAP", then=Value(3)),
            When(badge="Local", then=Value(4)),
            When(badge="Thuần chay", then=Value(5)),
            When(badge="Non-GMO", then=Value(6)),
            default=Value(7),
            output_field=IntegerField()
        )
    ).order_by("priority", "-created_at")
    farms = Farm.objects.filter(status='APPROVED')
    blogs = BlogPost.objects.all()
    
    # Optional server-side search/filter fallback
    q = request.GET.get("q")
    if q:
        products = products.filter(name__icontains=q) | products.filter(origin__icontains=q)
        
    total_farms = Farm.objects.filter(status='APPROVED').count()
    total_products = Product.objects.filter(status='APPROVED', farm__status='APPROVED').count()
    total_customers = CustomUser.objects.filter(is_staff=False).count()
    
    favorited_product_ids = []
    if request.user.is_authenticated:
        favorited_product_ids = list(request.user.favorites.values_list('product_id', flat=True))
        
    context = {
        "categories": categories,
        "products": products,
        "farms": farms,
        "blogs": blogs,
        "total_farms": total_farms,
        "total_products": total_products,
        "total_customers": total_customers,
        "favorited_product_ids": favorited_product_ids,
    }
    return render(request, "home.html", context)

@login_required(login_url="/users/login/")
def favorites_list(request):
    favorites = FavoriteProduct.objects.filter(user=request.user).select_related('product')
    return render(request, "products/favorites.html", {"favorites": favorites})

@login_required(login_url="/users/login/")
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    fav, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)
    if not created:
        fav.delete()
        messages.success(request, f"Đã xóa {product.name} khỏi danh sách yêu thích.")
    else:
        messages.success(request, f"Đã thêm {product.name} vào danh sách yêu thích.")
    return redirect(request.META.get("HTTP_REFERER", "/"))

from apps.farm.blockchain import get_batch_journey_from_blockchain
from django.http import JsonResponse

def trace_batch_api(request, batch_id):
    """
    API endpoint và trang web truy xuất hành trình lô sản phẩm trực tiếp từ Blockchain.
    """
    journey = get_batch_journey_from_blockchain(batch_id)
    
    # Hỗ trợ API JSON (tương thích ngược cho các modal hiện tại)
    if request.GET.get('format') == 'json' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "success": True,
            "batch_id": batch_id,
            "journey": journey
        })
        
    # Render trang web công khai đầy đủ (cho khách hàng quét QR)
    batch = get_object_or_404(Batch, batch_number=batch_id)
    
    if not journey:
        journey = {
            "batch_id": batch.batch_number,
            "product_name": batch.product.name,
            "farm_name": batch.product.farm.name if batch.product.farm else "",
            "milestones": [],
            "delivery_hashes": []
        }
        for m in batch.milestones.filter(status="VERIFIED").order_by("timestamp"):
            journey["milestones"].append({
                "title": m.title,
                "description": m.description,
                "location": m.location,
                "actor": m.actor,
                "timestamp": m.timestamp,
                "blockchain_tx_hash": m.blockchain_tx_hash,
                "parameters": m.parameters
            })
    else:
        # Đồng bộ thông tin TxHash và parameters từ database cho các mốc từ Blockchain
        db_milestones = list(batch.milestones.all().order_by("timestamp"))
        for idx, m in enumerate(journey["milestones"]):
            if idx < len(db_milestones):
                m["blockchain_tx_hash"] = db_milestones[idx].blockchain_tx_hash
                m["parameters"] = db_milestones[idx].parameters
            else:
                m["blockchain_tx_hash"] = ""
                m["parameters"] = {}
                
    product = batch.product
    category_slug = product.category.slug if product.category else "other"
    
    # Cấu hình bảng màu và hình ảnh Unsplash theo danh mục sản phẩm
    if category_slug == 'sua':
        bg_color = "#F8FAFC"
        text_color = "#0A1C2A"
        primary_color = "#0284C7"
        secondary_color = "#E0F2FE"
        accent_color = "#0369A1"
        primary_rgb = "2, 132, 199"
        accent_rgb = "3, 105, 161"
        theme_banner = "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=800&auto=format&fit=crop"
    elif category_slug in ['ca-phe', 'tra']:
        bg_color = "#FAF6F0"
        text_color = "#2D1E12"
        primary_color = "#F5A300"
        secondary_color = "#FDF6E2"
        accent_color = "#8B5A2B"
        primary_rgb = "245, 163, 0"
        accent_rgb = "139, 90, 43"
        theme_banner = "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&auto=format&fit=crop"
    else: # rau-cu-qua, trai-cay, gao, hat, other
        bg_color = "#F4F9F1"
        text_color = "#1A3020"
        primary_color = "#007A36"
        secondary_color = "#E4F2DB"
        accent_color = "#F5A300"
        primary_rgb = "0, 122, 54"
        accent_rgb = "245, 163, 0"
        theme_banner = "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=800&auto=format&fit=crop"

    return render(request, "products/trace_journey.html", {
        "batch": batch,
        "product": product,
        "category_slug": category_slug,
        "journey": journey,
        "bg_color": bg_color,
        "text_color": text_color,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "accent_color": accent_color,
        "primary_rgb": primary_rgb,
        "accent_rgb": accent_rgb,
        "theme_banner": theme_banner,
    })

from apps.farm.blockchain import get_recent_blockchain_transactions

def blockchain_explorer(request):
    """
    Trang thông tin trình khám phá khối Blockchain (Block Explorer).
    """
    transactions = get_recent_blockchain_transactions()
    return render(request, "products/explorer.html", {"transactions": transactions})


def get_tx_details_api(request, tx_hash):
    """
    API endpoint trả về chi tiết một giao dịch trên Blockchain dạng JSON.
    """
    import datetime
    from django.utils import timezone
    from apps.farm.blockchain import get_web3_connection
    from apps.products.models import Batch, BatchMilestone
    w3 = get_web3_connection()
    
    # Chuẩn hóa để query DB (không có 0x) và query Web3 (có 0x)
    db_tx_hash = tx_hash[2:] if tx_hash.lower().startswith('0x') else tx_hash
    web3_tx_hash = tx_hash if tx_hash.lower().startswith('0x') else '0x' + tx_hash
    
    # Chuẩn bị dữ liệu decoder trước từ database
    decoder_info = None
    milestone = BatchMilestone.objects.filter(blockchain_tx_hash__iexact=db_tx_hash).select_related('batch__product__farm').first()
    if milestone:
        decoder_info = {
            "type": "milestone",
            "title": milestone.title,
            "description": milestone.description,
            "farm_name": milestone.batch.product.farm.name,
            "product_name": milestone.batch.product.name,
            "batch_code": milestone.batch.batch_number
        }
    else:
        batch = Batch.objects.filter(blockchain_tx_hash__iexact=db_tx_hash).select_related('product__farm').first()
        if batch:
            decoder_info = {
                "type": "batch_creation",
                "title": "Khởi tạo lô hàng nông sản sạch",
                "description": f"Khởi tạo lô hàng mã {batch.batch_number} với số lượng gieo giống ban đầu: {batch.initial_quantity} {batch.product.unit}.",
                "farm_name": batch.product.farm.name,
                "product_name": batch.product.name,
                "batch_code": batch.batch_number
            }
            
    # Thử kết nối Web3 và lấy thông tin Blockchain thực tế
    try:
        if not w3:
            raise Exception("Không thể kết nối mạng Blockchain")
            
        tx = w3.eth.get_transaction(web3_tx_hash)
        receipt = w3.eth.get_transaction_receipt(web3_tx_hash)
        
        block = w3.eth.get_block(tx.blockNumber)
        block_time = datetime.datetime.fromtimestamp(block.timestamp).strftime('%H:%M:%S %d/%m/%Y')
        
        status = "Success" if receipt.status == 1 else "Failed"
        gas_used = receipt.gasUsed
        to_addr = receipt.contractAddress if receipt.contractAddress else tx.to
        if not to_addr:
            to_addr = "Hợp đồng mới"
            
        return JsonResponse({
            "success": True,
            "tx_hash": web3_tx_hash,
            "block_number": tx.blockNumber,
            "timestamp": block_time,
            "from_addr": tx["from"],
            "to_addr": to_addr,
            "gas_used": gas_used,
            "status": status,
            "decoder": decoder_info
        })
    except Exception as e:
        # Cơ chế Fallback: Nếu lỗi Blockchain (ví dụ Transaction not found do Hardhat node reset)
        # nhưng chúng ta vẫn có thông tin trong DB thì vẫn trả về thành công kèm decoder!
        if decoder_info:
            now_str = timezone.localtime(timezone.now()).strftime('%H:%M:%S %d/%m/%Y')
            return JsonResponse({
                "success": True,
                "tx_hash": web3_tx_hash,
                "block_number": "N/A (Chuỗi thử nghiệm đã reset)",
                "timestamp": now_str,
                "from_addr": "N/A (Dữ liệu cũ trên Testnet)",
                "to_addr": "N/A (Dữ liệu cũ trên Testnet)",
                "gas_used": 0,
                "status": "Success (Bảo chứng bởi DB)",
                "decoder": decoder_info,
                "warning": "Giao dịch cũ trên chuỗi thử nghiệm Hardhat cục bộ đã bị xóa sạch do node reset, tuy nhiên tính hợp lệ của dữ liệu vẫn được bảo toàn và bảo chứng bởi Database hệ thống."
            })
        
        return JsonResponse({"success": False, "error": f"Lỗi truy vấn Sổ cái: {str(e)}"}, status=400)
