from django.contrib import admin
from .models import Vendor, Customer, Product, Order


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    list_display = ["user", "location", "is_approved"]
    list_filter = ["is_approved"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ["user", "created_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "vendor", "price"]
    list_filter = ["vendor"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "vendor",
        "product",
        "quantity",
        "total_price",
        "status",
        "created_at",
    ]
    list_filter = ["status", "vendor"]
