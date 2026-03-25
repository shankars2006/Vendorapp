from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Vendor model
class Vendor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    location = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# Product Model
class Product(models.Model):
    CATEGORY_CHOICES = [
        ("fruits_veg", "Fruits and Vegetables"),
        ("snacks", "Snacks"),
        ("packed_food", "Packed Food"),
        ("electronics", "Electronics"),
        ("stationaries", "Stationaries"),
        ("dairy", "Dairy Items"),
        ("dress", "Dress"),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to="products/")
    
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="food")
    unit_or_size = models.CharField(max_length=50, blank=True, null=True)  # Sizes or 'KGs'

    def __str__(self):
        return self.name


# Customer model
class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_size = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ("pickup", "Pickup Order"),
        ("dispatch", "Dispatch"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("return_requested", "Return Requested"),
        ("returned", "Returned"),
        ("claim_requested", "Claim Requested"),
        ("claimed", "Amount Claimed"),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendor_orders")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    selected_size = models.CharField(max_length=20, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField(null=True, blank=True)

    # --- ADD THESE NEW FIELDS ---
    payment_method = models.CharField(max_length=20, default="card")
    payment_card_name = models.CharField(max_length=255, blank=True, null=True)
    payment_card_number = models.CharField(max_length=20, blank=True, null=True)
    payment_card_exp = models.CharField(max_length=10, blank=True, null=True)
    payment_card_cvv = models.CharField(max_length=10, blank=True, null=True)
    payment_upi_screenshot = models.ImageField(upload_to="payments/", blank=True, null=True)
    # ----------------------------

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pickup")
    created_at = models.DateTimeField(auto_now_add=True)

    delivery_person_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_person_mobile = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name if self.product else 'Unknown'}"


class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 Star - Poor"),
        (2, "2 Stars - Fair"),
        (3, "3 Stars - Good"),
        (4, "4 Stars - Very Good"),
        (5, "5 Stars - Excellent"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.customer.username}"
