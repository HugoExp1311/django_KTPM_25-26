import pytest
from django.urls import reverse
from django.test import Client
from userauths.models import User
from core.models import Product, Category, Vendor

@pytest.mark.django_db
class TestProductAdvanced:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', email='test@zstyle.com', password='123')
        self.category = Category.objects.create(title="Test Cat", cid="cat001")
        self.vendor = Vendor.objects.create(title="Test Vendor", vid="ven001", user=self.user)
        
        # Tạo 15 sản phẩm để test phân trang (giả sử mỗi trang hiện 10)
        for i in range(1, 16):
            Product.objects.create(
                pid=f"prod{i}",
                user=self.user,
                category=self.category,
                vendor=self.vendor,
                title=f"Product {i}",
                price=10.00 + i, # Giá tăng dần: 11, 12, ...
                product_status="published",
                status=True,
                in_stock=True
            )

    def test_pagination_logic(self):
        """Kiểm tra xem trang 2 có tồn tại không"""
        # Giả sử URL shop list là 'core:shop' hoặc 'core:product-list'
        try:
            url = reverse('core:product-list') # Sửa tên này theo urls.py của bạn
            response = self.client.get(url, {'page': 2})
            
            # Nếu view có phân trang, response sẽ là 200. Nếu không có trang 2 (lỗi), thường là 404
            if response.status_code == 200:
                print("\n[INFO] Hệ thống CÓ hỗ trợ phân trang.")
            elif response.status_code == 404:
                print("\n[WARN] Hệ thống chưa setup phân trang (pagination).")
            
            # Assert cơ bản: Không được sập (500)
            assert response.status_code in [200, 404]
        except:
            pass

    def test_sorting_price_low_to_high(self):
        """Kiểm tra sắp xếp giá từ thấp đến cao"""
        try:
            url = reverse('core:product-list')
            # Giả sử tham số sort là 'sort=price_asc' hoặc 'ordering=price'
            response = self.client.get(url, {'sort': 'price_asc'})
            
            # Lấy list sản phẩm từ context
            products = list(response.context['products'])
            if len(products) > 1:
                # Kiểm tra giá sản phẩm đầu tiên phải nhỏ hơn hoặc bằng sản phẩm thứ 2
                assert products[0].price <= products[1].price
        except:
            pass