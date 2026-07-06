from django.contrib import admin
from .models import Category, Farm, Product, BlogCategory, BlogPost, Batch, BatchMilestone

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "owner", "approved"]
    list_filter = ["approved"]
    search_fields = ["name", "region"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.approved and obj.owner:
            obj.owner.role = "FARMER"
            obj.owner.save()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "unit", "farm", "available", "rating"]
    list_filter = ["category", "available", "badge"]
    search_fields = ["name", "origin"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ["batch_number", "product", "initial_quantity", "remaining_quantity", "status", "seeding_date", "harvest_date"]
    list_filter = ["status", "product__farm"]
    search_fields = ["batch_number", "product__name"]

@admin.register(BatchMilestone)
class BatchMilestoneAdmin(admin.ModelAdmin):
    list_display = ["batch", "title", "location", "actor", "timestamp"]
    search_fields = ["batch__batch_number", "title"]

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "published_date"]
    list_filter = ["category"]
    search_fields = ["title", "summary", "content"]
    prepopulated_fields = {"slug": ("title",)}

