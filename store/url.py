# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    # Thêm các URL mới
    path('order-history/', views.order_history, name="order_history"),
    path('order-detail/<int:order_id>/', views.order_detail, name="order_detail"),
]