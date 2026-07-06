from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomUser

def get_login_redirect_url(user):
    if user.is_staff or user.role == "ADMIN":
        return "admin-reports"
    elif user.role == "AUDITOR":
        return "farm:auditor_dashboard"
    elif user.role == "FARMER":
        from apps.products.models import Farm
        try:
            farm = Farm.objects.get(owner=user)
            if farm.status == "APPROVED" or farm.status == "SUSPENDED":
                return "farm:dashboard"
            else:
                return "farm:home"
        except Farm.DoesNotExist:
            return "farm:home"
    return "home"

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "BUYER")
        phone_number = request.POST.get("phone_number", "")
        address = request.POST.get("address", "")
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại.")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                phone_number=phone_number,
                address=address
            )
            login(request, user)
            messages.success(request, f"Đăng ký tài khoản thành công! Chào mừng {username}.")
            return redirect(get_login_redirect_url(user))
            
    return render(request, "users/signup.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_login_redirect_url(request.user))
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Chào mừng quay trở lại, {username}!")
            return redirect(get_login_redirect_url(user))
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác.")
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công.")
    return redirect("home")

@login_required(login_url="/users/login/")
def profile_view(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")
        user.phone_number = request.POST.get("phone_number", "")
        user.address = request.POST.get("address", "")
        user.save()
        messages.success(request, "Cập nhật hồ sơ cá nhân thành công!")
        return redirect("users:profile")
    return render(request, "users/profile.html", {"user": user})
