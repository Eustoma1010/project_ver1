from django.urls import path
from . import views

app_name = "farm"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:pk>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:pk>/", views.delete_product, name="delete_product"),
    path("batches/", views.batches_list, name="batches"),
    path("batches/add/", views.add_batch, name="add_batch"),
    path("batches/milestone/add/<int:batch_id>/", views.add_milestone, name="add_milestone"),
    path("batches/harvest/<int:batch_id>/", views.harvest_batch, name="harvest_batch"),
    path("batches/simulate_iot/<int:batch_id>/", views.simulate_iot, name="simulate_iot"),
    path("auditor/dashboard/", views.auditor_dashboard, name="auditor_dashboard"),
]
