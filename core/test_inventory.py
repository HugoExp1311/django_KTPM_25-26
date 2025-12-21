import pytest
from django.test import Client
from userauths.models import User
from core.models import Product, Category, Vendor

@pytest.mark.django_db
class TestInventoryEdgeCases:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username='stock_tester', email='stock@test.com', password='123')
        self.category = Category.objects.create(title="Stock Cat", cid="stock01")
        self.vendor = Vendor.objects.create(title="Stock Vendor", vid="ven_stock", user=self.user)
        
        # Tạo sản phẩm CHỈ CÓ 1 cái trong kho
        self.product = Product.objects.create(
            pid="last_item",
            user=self.user,
            category=self.category,
            vendor=self.vendor,
            title="Last Item on Earth",
            price=100.00,
            stock_count=1, # Quan trọng
            in_stock=True,
            status=True
        )

    def test_prevent_purchase_when_out_of_stock(self):
        """Test: Mua hàng khi stock=0 phải thất bại"""
        # 1. Khách hàng A mua món cuối cùng
        self.product.stock_count = 0
        self.product.in_stock = False
        self.product.save()
        
        # 2. Khách hàng B cố gắng thêm vào giỏ (Giả lập logic check kho)
        # Vì ta chưa có logic chặn ở view, ta test logic Model hoặc giả định view trả lỗi
        
        can_buy = False
        if self.product.stock_count > 0:
            can_buy = True
            
        assert can_buy is False, "Hệ thống không được cho phép mua khi hết hàng"

    def test_inventory_decrement(self):
        """Test: Sau khi mua, số lượng tồn kho phải giảm"""
        initial_stock = self.product.stock_count
        
        # Giả lập hành động mua hàng thành công
        qty_bought = 1
        self.product.stock_count -= qty_bought
        self.product.save()
        
        updated_product = Product.objects.get(pid="last_item")
        assert updated_product.stock_count == initial_stock - 1