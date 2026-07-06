from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.success_view, name="success"),
    path("my-orders/", views.my_orders, name="my-orders"),
]
