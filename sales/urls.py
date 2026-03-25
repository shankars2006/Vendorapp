from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.index, name="index"),
    # Vendor
    path("vendor-register/", views.vendor_register, name="vendor_register"),
    path("vendor-login/", views.vendor_login, name="vendor_login"),
    path("vendor-dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path(
        "update-order-status/<int:order_id>/",
        views.update_order_status,
        name="update_order_status",
    ),
    # Custom Admin
    path("ad/", views.custom_admin_dashboard, name="ad"),
    path(
        "toggle-vendor/<int:vendor_id>/",
        views.toggle_vendor_approval,
        name="toggle_vendor_approval",
    ),
    # Customer
    path("customer-register/", views.customer_register, name="customer_register"),
    path("customer-login/", views.customer_login, name="customer_login"),
    path("customer-dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("add-product/", views.add_product, name="add_product"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("increase-quantity/<int:cart_id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease-quantity/<int:cart_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    # Wishlist
    path("add-to-wishlist/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove-from-wishlist/<int:wishlist_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("move-to-cart/<int:wishlist_id>/", views.move_to_cart, name="move_to_cart"),
    path("add-all-to-cart/", views.add_all_to_cart, name="add_all_to_cart"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("logout/", views.user_logout, name="logout"),
    path("edit-product/<int:product_id>/", views.edit_product, name="edit_product"),
    path(
        "delete-product/<int:product_id>/", views.delete_product, name="delete_product"
    ),
    path("product-detail/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cancel-order/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("reorder/<int:order_id>/", views.reorder, name="reorder"),
    path("return-order/<int:order_id>/", views.return_order, name="return_order"),
    path("vendor-process-return/<int:order_id>/<str:action>/", views.vendor_process_return, name="vendor_process_return"),
    path("submit-review/<int:product_id>/", views.submit_review, name="submit_review"),
    path("approve-claim/<int:order_id>/", views.approve_claim, name="approve_claim"),
    path("request-claim/<int:order_id>/", views.request_claim, name="request_claim"),
]
