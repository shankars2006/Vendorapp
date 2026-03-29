from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Avg
from decimal import Decimal
from .models import Vendor, Product, Customer, Order, Cart, Wishlist, Review, Payout
from .forms import (
    VendorRegisterForm,
    VendorLoginForm,
    CustomerRegisterForm,
    CustomerLoginForm,
    ProductForm,
    ReviewForm,
)

# Create your views here.


# INDEX PAGE → SHOW PRODUCTS
def index(request):
    products = Product.objects.select_related("vendor", "vendor__user").annotate(avg_rating=Avg('reviews__rating'))
    cart_count = 0

    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0

    return render(
        request, "sales/index.html", {"products": products, "cart_count": cart_count}
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().select_related('customer')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    cart_count = 0
    has_purchased = False
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        has_purchased = Order.objects.filter(customer=request.user, product=product).exists()
    
    return render(request, "sales/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "cart_count": cart_count,
        "has_purchased": has_purchased
    })


@login_required(login_url="sales:customer_login")
@login_required(login_url="sales:customer_login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.quantity == 0:
        return redirect("sales:product_detail", product_id=product_id)
        
    quantity = int(request.POST.get("quantity", 1))
    selected_size = request.POST.get("selected_size", None)
    
    # Check if item with same size already exists in cart for this user
    cart_item = Cart.objects.filter(user=request.user, product=product, selected_size=selected_size).first()
    
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            selected_size=selected_size
        )

    return redirect("sales:cart")


@login_required(login_url="sales:customer_login")
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity < cart_item.product.quantity:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("sales:cart")


@login_required(login_url="sales:customer_login")
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("sales:cart")


@login_required(login_url="sales:customer_login")
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "sales/cart.html", {"cart_items": cart_items, "total": total})

# CHECKOUT
@login_required(login_url="sales:customer_login")
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')

    if not cart_items:
        return redirect("sales:index")

    if request.method == "POST":
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method", "card")
        card_name = request.POST.get("card_name", "")
        card_number = request.POST.get("card_number", "")
        card_exp = request.POST.get("card_exp", "")
        card_cvv = request.POST.get("card_cvv", "")
        upi_screenshot = request.FILES.get("upi_screenshot")

        # Validate form based on payment method
        error = None
        if not address:
            error = "Delivery address is profoundly required."
        elif payment_method == "card" and not all([card_name, card_number, card_exp, card_cvv]):
            error = "All credit/debit card details must be securely provided."
        elif payment_method == "upi" and not upi_screenshot:
            error = "A valid UPI transaction screenshot must be uploaded for verification."
        elif payment_method == "cod":
            # Clear arbitrary data if COD is somehow injected
            card_name, card_number, card_exp, card_cvv, upi_screenshot = "", "", "", "", None
        elif payment_method not in ["card", "upi", "cod"]:
            error = "Invalid payment method selected."

        if error:
            total = sum(item.product.price * item.quantity for item in cart_items)
            return render(request, "sales/checkout.html", {"total": total, "items": cart_items, "error": error})

        for item in cart_items:
            Order.objects.create(
                product=item.product,
                vendor=item.product.vendor.user,
                customer=request.user,
                quantity=item.quantity,
                selected_size=item.selected_size,
                total_price=item.product.price * item.quantity,
                status="pickup",
                delivery_address=address,
                payment_method=payment_method,
                payment_card_name=card_name,
                payment_card_number=card_number,
                payment_card_exp=card_exp,
                payment_card_cvv=card_cvv,
                payment_upi_screenshot=upi_screenshot,
            )
            
            # Deduct stock
            item.product.quantity -= item.quantity
            item.product.save()

        # Clear cart
        cart_items.delete()
        return render(request, "sales/order_success.html")

    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "sales/checkout.html", {"total": total, "items": cart_items})


# -------------------------
# VENDOR REGISTER
# -------------------------
def vendor_register(request):

    if request.method == "POST":

        form = VendorRegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            Vendor.objects.create(
                user=user, 
                location=form.cleaned_data["location"],
                mobile_number=form.cleaned_data["mobile_number"],
                email=form.cleaned_data["email"],
                is_approved=False
            )

            return render(request, "sales/vendor_pending.html")

    else:
        form = VendorRegisterForm()

    return render(request, "sales/vendor_register.html", {"form": form})


# -------------------------
# VENDOR LOGIN
# -------------------------
def vendor_login(request):

    if request.method == "POST":

        form = VendorLoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:

                vendor = Vendor.objects.filter(user=user).first()

                if not vendor:
                    return render(
                        request,
                        "sales/vendor_login.html",
                        {"form": form, "error": "Vendor not found"},
                    )

                if not vendor.is_approved:
                    return render(
                        request,
                        "sales/vendor_login.html",
                        {"form": form, "error": "Waiting for admin approval"},
                    )

                login(request, user)
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("sales:vendor_dashboard")

            else:
                return render(
                    request,
                    "sales/vendor_login.html",
                    {"form": form, "error": "Invalid credentials"},
                )

    else:
        form = VendorLoginForm()

    return render(request, "sales/vendor_login.html", {"form": form})


# -------------------------
# CUSTOM ADMIN DASHBOARD
# -------------------------
@staff_member_required
def custom_admin_dashboard(request):

    # Most Sold Products (by quantity)
    # Order.product might be null, so exclude them
    top_products = (
        Order.objects.exclude(product__isnull=True)
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    product_names = [p["product__name"] for p in top_products]
    product_sales = [p["total_sold"] for p in top_products]

    # Top Sellers (by Revenue)
    # vendor here refers to User.username because vendor is a User ForeignKey in Order.
    top_sellers = (
        Order.objects.values("vendor__username")
        .annotate(total_revenue=Sum("total_price"))
        .order_by("-total_revenue")[:5]
    )

    seller_names = [s["vendor__username"] for s in top_sellers]
    seller_revenue = [
        float(s["total_revenue"]) if s["total_revenue"] else 0.0 for s in top_sellers
    ]

    # Fetch all vendors for approval table
    vendors = Vendor.objects.select_related("user").all().order_by("-id")

    # Calculate earnings and pending balances for vendors in real-time
    for v in vendors:
        orders = Order.objects.filter(vendor=v.user, status__in=['delivered', 'claimed'])
        gross = orders.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
        net = gross * Decimal('0.90')
        paid = Payout.objects.filter(vendor=v).aggregate(total=Sum('net_payout'))['total'] or Decimal('0.00')
        pending = max(Decimal('0.00'), net - paid)

        v.total_gross = gross
        v.total_net = net
        v.total_paid = paid
        v.pending_balance = pending
        
        # Attach historical itemized orders array for the invoice logic
        v.invoice_orders = Order.objects.filter(vendor=v.user).exclude(status__in=['pickup', 'dispatch', 'out_for_delivery']).order_by('-created_at')

    context = {
        "product_names": product_names,
        "product_sales": product_sales,
        "seller_names": seller_names,
        "seller_revenue": seller_revenue,
        "vendors": vendors,
    }

    return render(request, "sales/custom_admin_dashboard.html", context)


@staff_member_required
def toggle_vendor_approval(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    vendor.is_approved = not vendor.is_approved
    vendor.save()
    return redirect("sales:ad")


@staff_member_required
def process_payout(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    if not vendor.bank_name or not vendor.account_number:
        return redirect("sales:ad")
        
    orders = Order.objects.filter(vendor=vendor.user, status__in=['delivered', 'claimed'])
    gross = orders.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
    net = gross * Decimal('0.90')
    
    paid = Payout.objects.filter(vendor=vendor).aggregate(total=Sum('net_payout'))['total'] or Decimal('0.00')
    pending = max(Decimal('0.00'), net - paid)
    
    if pending > Decimal('0.00'):
        payout_gross = pending / Decimal('0.90')
        payout_fee = payout_gross * Decimal('0.10')
        Payout.objects.create(
            vendor=vendor,
            gross_volume=payout_gross,
            platform_fee=payout_fee,
            net_payout=pending
        )
        
    return redirect("sales:ad")


@staff_member_required
def delete_unapproved_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    # Only allow deletion if the vendor is explicitly unapproved
    if not vendor.is_approved:
        user = vendor.user
        vendor.delete()
        user.delete()
    return redirect("sales:ad")


@login_required(login_url="sales:vendor_login")
def vendor_invoice(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    
    # Secure endpoint: only admin or the specific vendor can access their invoice
    if not request.user.is_staff and request.user != vendor.user:
        return redirect("sales:index")
        
    orders_earned = Order.objects.filter(vendor=vendor.user, status__in=['delivered', 'claimed'])
    total_gross = orders_earned.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
    total_net = total_gross * Decimal('0.90')
    total_fee = total_gross - total_net
    
    total_paid = Payout.objects.filter(vendor=vendor).aggregate(total=Sum('net_payout'))['total'] or Decimal('0.00')
    pending_balance = max(Decimal('0.00'), total_net - total_paid)
    
    invoice_orders = Order.objects.filter(vendor=vendor.user).exclude(status__in=['pickup', 'dispatch', 'out_for_delivery']).order_by('-created_at')

    return render(request, "sales/invoice.html", {
        "vendor": vendor,
        "total_gross": total_gross,
        "total_fee": total_fee,
        "total_net": total_net,
        "pending_balance": pending_balance,
        "invoice_orders": invoice_orders
    })


# Customer Handlers moved to bottom of file


# Add Product
def add_product(request):

    vendor = Vendor.objects.get(user=request.user)

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)

            product.vendor = vendor

            product.save()

            return redirect("sales:vendor_dashboard")

    else:

        form = ProductForm()

    return render(request, "sales/add_product.html", {"form": form})


# -------------------------
# DASHBOARDS
# -------------------------
def vendor_dashboard(request):

    vendor = Vendor.objects.get(user=request.user)

    products = Product.objects.filter(vendor=vendor).annotate(
        avg_rating=Avg('reviews__rating')
    ).prefetch_related('reviews__customer')

    orders = Order.objects.filter(
        vendor=request.user
    ).select_related(
        "product",
        "customer"
    ).order_by("-created_at")

    active_orders = orders.exclude(status__in=['delivered', 'cancelled', 'returned', 'return_requested', 'claim_requested', 'claimed'])
    history_orders = orders.filter(status='delivered')
    cancelled_orders = orders.filter(status='cancelled')
    return_requests = orders.filter(status='return_requested')
    returned_history = orders.filter(status='returned')
    claim_requests = orders.filter(status='claim_requested')
    claimed_history = orders.filter(status='claimed')

    orders_earned = orders.filter(status__in=['delivered', 'claimed'])
    total_gross = orders_earned.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
    total_net = total_gross * Decimal('0.90')
    total_fee = total_gross - total_net
    
    total_paid = Payout.objects.filter(vendor=vendor).aggregate(total=Sum('net_payout'))['total'] or Decimal('0.00')
    pending_balance = max(Decimal('0.00'), total_net - total_paid)
    payouts = Payout.objects.filter(vendor=vendor).order_by('-created_at')
    invoice_orders = orders.exclude(status__in=['pickup', 'dispatch', 'out_for_delivery']).order_by('-created_at')

    return render(request, "sales/vendor_dashboard.html", {
        "vendor": vendor,
        "products": products,
        "active_orders": active_orders,
        "history_orders": history_orders,
        "cancelled_orders": cancelled_orders,
        "return_requests": return_requests,
        "returned_history": returned_history,
        "claim_requests": claim_requests,
        "claimed_history": claimed_history,
        "total_gross": total_gross,
        "total_fee": total_fee,
        "total_net": total_net,
        "total_paid": total_paid,
        "pending_balance": pending_balance,
        "payouts": payouts,
        "invoice_orders": invoice_orders
    })


@login_required(login_url="sales:vendor_login")
def update_bank_details(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        vendor.bank_name = request.POST.get('bank_name')
        vendor.account_number = request.POST.get('account_number')
        vendor.ifsc_code = request.POST.get('ifsc_code')
        vendor.save()
    return redirect("sales:vendor_dashboard")


@login_required(login_url="sales:vendor_login")
def update_order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id, vendor=request.user)

    if request.method == "POST":
        status_map = {
            "pickup": "dispatch",
            "dispatch": "out_for_delivery",
            "out_for_delivery": "delivered",
        }
        
        current_status = order.status
        next_status = status_map.get(current_status)
        
        if next_status:
            if next_status == "out_for_delivery":
                order.delivery_person_name = request.POST.get("delivery_person_name")
                order.delivery_person_mobile = request.POST.get("delivery_person_mobile")
            
            order.status = next_status
            order.save()

    return redirect("sales:vendor_dashboard")


@login_required(login_url="sales:customer_login")
def customer_dashboard(request):
    orders = Order.objects.filter(
        customer=request.user
    ).select_related(
        "product", 
        "vendor"
    ).order_by("-created_at")

    active_orders = orders.exclude(status__in=['delivered', 'cancelled', 'returned', 'return_requested'])
    history_orders = orders.filter(status__in=['delivered', 'returned', 'return_requested'])
    cancelled_orders = orders.filter(status='cancelled')

    return render(request, "sales/customer_dashboard.html", {
        "active_orders": active_orders,
        "history_orders": history_orders,
        "cancelled_orders": cancelled_orders
    })


@login_required(login_url="sales:customer_login")
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.status == 'pickup':
        order.status = 'cancelled'
        order.save()
        # Restore stock
        if order.product:
            order.product.quantity += order.quantity
            order.product.save()
    return redirect("sales:customer_dashboard")


@login_required(login_url="sales:customer_login")
def reorder(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.product:
        Cart.objects.get_or_create(
            user=request.user,
            product=order.product,
            selected_size=order.selected_size,
            defaults={'quantity': order.quantity}
        )
    return redirect("sales:cart")


@login_required(login_url="sales:customer_login")
def return_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.status == 'delivered':
        order.status = 'return_requested'
        order.save()
    return redirect("sales:customer_dashboard")


@login_required(login_url="sales:vendor_login")
def vendor_process_return(request, order_id, action):
    order = get_object_or_404(Order, id=order_id, vendor=request.user)
    if order.status == 'return_requested':
        order.status = 'returned'
        order.save()
        if action == 'update_stock':
            if order.product:
                order.product.quantity += order.quantity
                order.product.save()
    return redirect("sales:vendor_dashboard")


@login_required(login_url="sales:customer_login")
def request_claim(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.status == 'returned':
        order.status = 'claim_requested'
        order.save()
    return redirect("sales:customer_dashboard")


@login_required(login_url="sales:vendor_login")
def approve_claim(request, order_id):
    order = get_object_or_404(Order, id=order_id, vendor=request.user)
    if order.status == 'claim_requested':
        order.status = 'claimed'
        order.save()
    return redirect("sales:vendor_dashboard")


@login_required(login_url="sales:customer_login")
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        has_purchased = Order.objects.filter(customer=request.user, product=product).exists()
        if has_purchased:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.customer = request.user
                review.save()
    return redirect("sales:product_detail", product_id=product_id)


# -------------------------
# WISHLIST ACTIONS
# -------------------------
@login_required(login_url="sales:customer_login")
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    wishlist_total = sum(item.subtotal for item in wishlist_items)
    return render(request, "sales/wishlist.html", {
        "wishlist_items": wishlist_items,
        "wishlist_total": wishlist_total
    })


@login_required(login_url="sales:customer_login")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if exists
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if not wishlist_item:
        Wishlist.objects.create(user=request.user, product=product, quantity=1)
    
    return redirect("sales:wishlist")


@login_required(login_url="sales:customer_login")
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect("sales:wishlist")


@login_required(login_url="sales:customer_login")
def move_to_cart(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    
    # Add to cart (default quantity 1, size None for now as it's from wishlist)
    # If user wants to select size, they should go to detail page, but for now we move it
    Cart.objects.get_or_create(
        user=request.user,
        product=wishlist_item.product,
        defaults={'quantity': wishlist_item.quantity}
    )
    
    return redirect("sales:cart")


@login_required(login_url="sales:customer_login")
def add_all_to_cart(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    for item in wishlist_items:
        # Move to cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=item.product,
            defaults={'quantity': item.quantity}
        )
        if not created:
            cart_item.quantity += item.quantity
            cart_item.save()
            
    return redirect("sales:cart")


@login_required(login_url="sales:vendor_login")
def edit_product(request, product_id):

    vendor = Vendor.objects.get(user=request.user)

    product = get_object_or_404(Product, id=product_id, vendor=vendor)

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("sales:vendor_dashboard")

    else:
        form = ProductForm(instance=product)

    return render(request, "sales/edit_product.html", {"form": form})


@login_required(login_url="sales:vendor_login")
def delete_product(request, product_id):

    vendor = Vendor.objects.get(user=request.user)

    product = get_object_or_404(Product, id=product_id, vendor=vendor)

    product.delete()

    return redirect("sales:vendor_dashboard")


# -------------------------
# LOGOUT
# -------------------------
def user_logout(request):

    logout(request)

    return redirect("sales:index")


def customer_register(request):

    if request.method == "POST":

        form = CustomerRegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            Customer.objects.create(user=user)

            login(request, user)

            return redirect("sales:index")

    else:
        form = CustomerRegisterForm()

    return render(request, "sales/customer_register.html", {"form": form})


def customer_login(request):

    if request.method == "POST":

        form = CustomerLoginForm(request.POST)

        if form.is_valid():

            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user:

                login(request, user)

                next_url = request.GET.get("next", "sales:index")

                return redirect(next_url)

            else:
                return render(
                    request,
                    "sales/customer_login.html",
                    {"form": form, "error": "Invalid credentials"},
                )

    else:
        form = CustomerLoginForm()

    return render(request, "sales/customer_login.html", {"form": form})


def user_logout(request):

    logout(request)

    return redirect("sales:index")
